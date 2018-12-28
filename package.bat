set function_name=aws-lnkchk-log-stream-to-es
title %function_name%

call cd .\tests
call run_all_tests.bat
set test_error=%ERRORLEVEL%
call cd ..
IF %test_error%==1 goto failed_tests

call commit_and_push.bat
set test_error=%ERRORLEVEL%
IF %test_error%==1 goto failed_commit


REM Zip the lambda function
call del /q lambda_function.zip
call "c:\Program Files\7-Zip\7z.exe" a lambda_function.zip *.py
cd .\Lib\site-packages
call "c:\Program Files\7-Zip\7z.exe" a ..\..\lambda_function.zip *
cd ..\..\

REM Upload the new code
call aws lambda update-function-code --function-name %function_name% --zip-file fileb://lambda_function.zip
goto end

:failed_tests
echo *** Tests failed, so aborted packaging
goto end


:failed_commit
echo *** Commit failed, so aborted packaging
goto end

:end
echo %time% deployed 
