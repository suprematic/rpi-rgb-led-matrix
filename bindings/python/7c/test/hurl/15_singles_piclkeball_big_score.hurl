POST http://192.168.114.30:5000/score/xyz
Content-Type: application/json
{"client-id":"hurl-test",
"target-panels":["{{7c_target_panel}}"],
"isDoubles":false,
"hideServiceIndicator":true,
"isTeamEvent":false,
"t1name":"R.Federer",
"t2name":"E.Gulbis",
"t1":{"p1":{"colors":"","firstname":"Roger","flag":"","lastname":"Pickle"}},
"t2":{"p1":{"colors":"","firstname":"Ernests","flag":"","lastname":"Baller"}},
"t1serves":true,
"setScores":[{"first":11,"second":13}, {"first":15,"second":13}],
"gameScore":{"first":"17","second":"16"},
"matchStatus":"IN_GAME",
"description":"","authorName":"test","appVersion":"hurl-test","date":1672413885887,"userPlan":"FREE",
"appOS":"Android","matchCreationDate":1672402758432}