POST http://192.168.114.30:5000/score/xyz
Content-Type: application/json
{"client-id":"hurl-test",
"target-panels":["{{7c_target_panel}}"],
"isDoubles":true,
"isTeamEvent":false,
"t1name":"M.González/J.Carlos",
"t2name":"F.Portis/L.Jordan",
"t1":{"p1":{"colors":"","firstname":"Mario","flag":"","lastname":"González"},"p2":{"colors":"","firstname":"Juan","flag":"","lastname":"Carlos"}},
"t2":{"p1":{"colors":"","firstname":"Freddy","flag":"","lastname":"Portis"},"p2":{"colors":"","firstname":"Lui","flag":"","lastname":"Jordan"}},
"t1serves":null,
"setScores":[],
"gameScore":{"first":"0","second":"0"},
"matchStatus":"IN_GAME"}