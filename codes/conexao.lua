function coroutineMain()
    --estabelecendo conexao via ZMQ
    context=simZMQ.ctx_new()
    -- responder eh o server side
    responder=simZMQ.socket(context,simZMQ.REP)
    local rc=simZMQ.bind(responder,'tcp://*:5555')
    if rc~=0 then error('failed bind') end

    while true do
        local rc,data=simZMQ.recv(responder,0)
        if data == "get_active_joint_angle" then
            local joint_angles = angulo_junta(active_joint_handles)
            simZMQ.send(responder,joint_angles,0)
        end
    end
end