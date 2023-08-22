function sysCall_init()
    corout=coroutine.create(coroutineMain)
    
    --handlers    
    --joints ativos    
    simMotor1Joint=sim.getObject('./motor1')
    simMotor2Joint=sim.getObject('./motor2')
    simMotor3Joint=sim.getObject('./motor3')
    
    
    --joints passivos
    simauxJoint0=sim.getObject('./auxJoint0')
    simauxJoint1=sim.getObject('./auxJoint1')
    simauxJoint3=sim.getObject('./auxJoint3')
    simauxJoint4=sim.getObject('./auxJoint4')
    simauxJoint7=sim.getObject('./auxJoint7')
    simauxJoint8=sim.getObject('./auxJoint8')
    
    --joints passivos escritos como auxMotor
    simauxMotor1=sim.getObject('./auxMotor1')
    simauxMotor2=sim.getObject('./auxMotor2')
    
    --joints passivos escritos como dummy
    simloopDummy1A=sim.getObject('./dummy1A')
    simloopDummy1B=sim.getObject('./dummy1B')
    
    simloopDummy2A=sim.getObject('./dummy2A')
    simloopDummy2B=sim.getObject('./dummy2B')
    
    simloopDummy3A=sim.getObject('./dummy3A')
    simloopDummy3B=sim.getObject('./dummy3B')

    simTip = sim.getObject('./tip')
    simTarget = sim.getObject('./target')
    
    
   -- cinematic part
   -- Create a custom UI:
   
   ui=simUI.create([[<ui title="IK" closeable="false" placement="center">
   <label text="Motor1" />
   <hslider enabled="true" minimum="-100" maximum="100" id="1" on-change="onJ1Change" />
   <label text="Motor2" />
   <hslider enabled="true" minimum="-100" maximum="20" id="2" on-change="onJ2Change" />
   <label text="Motor3" />
   <hslider enabled="true" minimum="-80" maximum="50" id="3" on-change="onJ3Change" />
    </ui>]])


    jointHandles={-1,-1,-1}
    initialValues={0,0,0}
    for i=1,3,1 do
        jointHandles[i]=sim.getObjectHandle('./motor'..i)
        initialValues[i]=sim.getJointPosition(jointHandles[i])
    end
    local simBase=sim.getObject('./link1')
    ikEnv=simIK.createEnvironment()

    -- Prepare the main ik group, using the convenience function 'simIK.addElementFromScene':
    ikGroup=simIK.createGroup(ikEnv)
    simIK.setGroupCalculation(ikEnv,ikGroup,simIK.method_damped_least_squares,0.10,100)
    local ikElement=simIK.addElementFromScene(ikEnv,ikGroup,simBase,simloopDummy1A,simloopDummy1B,simIK.constraint_x+simIK.constraint_y+simIK.constraint_z)
    local ikElement=simIK.addElementFromScene(ikEnv,ikGroup,simBase,simloopDummy2A,simloopDummy2B,simIK.constraint_x+simIK.constraint_y+simIK.constraint_z+simIK.constraint_alpha_beta)
    local ikElement, simToIkObjectMap=simIK.addElementFromScene(ikEnv,ikGroup,simBase,simloopDummy3A,simloopDummy3B,simIK.constraint_x+simIK.constraint_y+simIK.constraint_z)
    simIK.setJointMode(ikEnv,simToIkObjectMap[simMotor1Joint],simIK.jointmode_passive) -- make sure that joint will act as 'rigid' during IK calculations
    simIK.setJointMode(ikEnv,simToIkObjectMap[simMotor2Joint],simIK.jointmode_passive) -- make sure that joint will act as 'rigid' during IK calculations
    simIK.setJointMode(ikEnv,simToIkObjectMap[simMotor3Joint],simIK.jointmode_passive) -- make sure that joint will act as 'rigid' during IK calculations
        
end

function onJ1Change(uiHandle, id, newValue)
    sim.setJointPosition(jointHandles[1],initialValues[1]+newValue*math.pi/200)
    
end
function onJ2Change(uiHandle, id, newValue)
    sim.setJointPosition(jointHandles[2],initialValues[2]+newValue*math.pi/200)
    
end
function onJ3Change(uiHandle, id, newValue)
    sim.setJointPosition(jointHandles[3],initialValues[3]+newValue*math.pi/200)
    
end

function sysCall_actuation()
    if coroutine.status(corout)~='dead' then
        local ok,errorMsg=coroutine.resume(corout)
        if errorMsg then
            error(debug.traceback(corout,errorMsg),2)
        end
    end

     -- Apply IK to the current scene, using the convenience function 'simIK.handleGroup':
     local result,failureReason=simIK.handleGroup(ikEnv,ikGroup,{syncWorlds=true, allowError=true})
     if result~=simIK.result_success then
         print('IK failed: '..simIK.getFailureDescription(failureReason))
     end
     --    simIK.handleGroup(ikEnv,ikGroup_fallback,{syncWorlds=true,allowError=true}) -- use the fall-back IK group if the main IK group failed
 
end

function sysCall_cleanup()
    -- Clean-up stuff:
    simIK.eraseEnvironment(ikEnv)
    simUI.destroy(ui)
    simZMQ.close(responder)
    simZMQ.ctx_term(context)
end

function coroutineMain()
    --estabelecendo conexao via ZMQ
    context=simZMQ.ctx_new()
    -- responder eh o server side
    responder=simZMQ.socket(context,simZMQ.REP)
    local rc=simZMQ.bind(responder,'tcp://*:5555')
    if rc~=0 then error('failed bind') end
    
    --
    local active_joint_handles = {
        simMotor1Joint,
        simMotor2Joint,
        simMotor3Joint,
        simauxMotor1,
    }
    
    while true do
        local rc,data=simZMQ.recv(responder,0)
        if data == "get_active_joint_angle" then
            local joint_angles = angulo_junta(active_joint_handles)
            simZMQ.send(responder,joint_angles,0)
        end
        
        if data == "set_active_joint_angle" then
            --reply the request
            simZMQ.send(responder, "Received set_active_joint_angle", 0)
            -- Esperar por outra mensagem com os valores dos angulos da junta
            local rc, joint_angles_str = simZMQ.recv(responder, 0)
            local joint_angles = stringToTable(joint_angles_str)
            print(joint_angles)
            for i=1, #joint_angles do
                local flag = sim.setJointPosition(active_joint_handles[i], joint_angles[i]*math.pi/180)
                if flag == -1 then
                    print(string.format("algo deu errado na junta %d", i))
                end
            end 
              simZMQ.send(responder, string.format("Angles received and aplied to joints"), 0)
        end

        if data == "get_end_efector_position" then
            local joint_position = {}
            local x, y, z = unpack(sim.getObjectPosition(simTip, sim.handle_world))
            local posicao_str = string.format("%.5f, %.5f, %.5f", x, y, z )
            table.insert(joint_position, posicao_str)
            local joint_positions = table.concat(joint_position, "\n")
            simZMQ.send(responder,joint_positions,0)
        end
    end
end


function angulo_junta (h)
    joint_angle = {}
    for i=1, #h do
        local angle = sim.getJointPosition(h[i])
        local angle_str = string.format("%.5f", angle * 180 / math.pi)
        table.insert(joint_angle, angle_str)   
    end
    
    local joint_angles = table.concat(joint_angle, "\n")
    return joint_angles
end


function stringToTable(str)
    local values = {}
    for value in string.gmatch(str, "[-+]?%d*%.?%d+") do
        table.insert(values, tonumber(value))
    end
    return values
end
-- See the user manual or the available code snippets for additional callback functions and details
