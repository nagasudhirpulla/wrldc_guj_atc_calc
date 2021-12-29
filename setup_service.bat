call nssm.exe install wr_guj_ttc_calc_service "%cd%\run_server.bat"
call nssm.exe set wr_guj_ttc_calc_service AppStdout "%cd%\logs\wr_guj_ttc_calc_service.log"
call nssm.exe set wr_guj_ttc_calc_service AppStderr "%cd%\logs\wr_guj_ttc_calc_service.log"
nssm set wr_guj_ttc_calc_service AppRotateFiles 1
nssm set wr_guj_ttc_calc_service AppRotateOnline 1
nssm set wr_guj_ttc_calc_service AppRotateSeconds 86400
nssm set wr_guj_ttc_calc_service AppRotateBytes 104857600
call sc start wr_guj_ttc_calc_service