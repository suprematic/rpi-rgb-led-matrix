POST http://192.168.114.30:5000/score/xyz
Content-Type: application/json
{"client-id":"hurl-test",
"target-panels":["{{7c_target_panel}}"],
"isDoubles":true,
"isTeamEvent":false,
"t1name":"M.González/J.Carlos",
"t2name":"F.Portis/L.Jordan",
"t1":{"p1":{"colors":"","firstname":"Mario","flag":"ukraine","lastname":"González"},"p2":{"colors":"","firstname":"Juan","flag":"argentina","lastname":"Carlos"}},
"t2":{"p1":{"colors":"","firstname":"Freddy","flag":"italy","lastname":"Portis"},"p2":{"colors":"","firstname":"Lui","flag":"spain","lastname":"Jordan"}},
"t1serves":true,
"setScores":[{"first":6,"second":2}, {"first":5,"second":7}, {"first":3,"second":5}],
"gameScore":{"first":"40","second":"A"},
"matchStatus":"IN_GAME",
"description":"","authorName":"test","appVersion":"hurl-test","date":1672413885887,"userPlan":"FREE",
"appOS":"Android","matchCreationDate":1672402758432}