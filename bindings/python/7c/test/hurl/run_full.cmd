SET TIMEOUT_SECONDS=4

hurl 00_acquire.hurl
00_singles_short.hurl
timeout %TIMEOUT_SECONDS%
10_singles_mid.hurl
timeout %TIMEOUT_SECONDS%
20_singles_long.hurl
timeout %TIMEOUT_SECONDS%
hurl 30_doubles_short_0th.hurl
timeout %TIMEOUT_SECONDS%
hurl 31_doubles_short_1st.hurl
timeout %TIMEOUT_SECONDS%
hurl 32_doubles_short_2nd.hurl
timeout %TIMEOUT_SECONDS%
hurl 33_doubles_short_3rd.hurl
timeout %TIMEOUT_SECONDS%
hurl 34_doubles_short_winner1.hurl
timeout %TIMEOUT_SECONDS%
hurl 35_doubles_short_winner2.hurl
timeout %TIMEOUT_SECONDS%
hurl 40_doubles_mid_0th.hurl
timeout %TIMEOUT_SECONDS%
hurl 41_doubles_mid_1st.hurl
timeout %TIMEOUT_SECONDS%
hurl 42_doubles_mid_2nd.hurl
timeout %TIMEOUT_SECONDS%
hurl 43_doubles_mid_3rd.hurl
timeout %TIMEOUT_SECONDS%
hurl 44_doubles_mid_winner1.hurl
timeout %TIMEOUT_SECONDS%
hurl 45_doubles_mid_winner2.hurl
timeout %TIMEOUT_SECONDS%
hurl 50_doubles_long_0th.hurl
timeout %TIMEOUT_SECONDS%
hurl 51_doubles_long_1st.hurl
timeout %TIMEOUT_SECONDS%
hurl 52_doubles_long_2nd.hurl
timeout %TIMEOUT_SECONDS%
hurl 53_doubles_long_3rd.hurl
timeout %TIMEOUT_SECONDS%
hurl 55_doubles_long_winner1.hurl
timeout %TIMEOUT_SECONDS%
hurl 55_doubles_long_winner2.hurl
timeout %TIMEOUT_SECONDS%
hurl 70_teams_doubles.hurl
timeout %TIMEOUT_SECONDS%
hurl 80_teams_singles.hurl
timeout %TIMEOUT_SECONDS%
hurl 99_release.hurl