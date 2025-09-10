local delay = math.random(100, 1000)
ngx.sleep(delay / 1000)

ngx.say("Hello! Simulated delay: " .. delay .. "ms")
