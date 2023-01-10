@echo off
SET TIMEOUT_SECONDS=2

:::: 7c-m1-r1
:: SET HURL_7c_target_panel=N0MtTTEtUjE=

:::: shinych's old thinkstation
:: SET HURL_7c_target_panel=dGhpbmtzdGF0aW9uMQ==

for %%i in (*.hurl) do (
    echo %%i
    hurl %%i
    timeout %TIMEOUT_SECONDS%
)