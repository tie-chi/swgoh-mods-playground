@echo off

set script_dir=%~dp0
set return_dir=%cd%
cd %script_dir%
set script_dir=%cd%

for %%F in (%script_dir%) do set "proj_dir=%%~dpF."
for %%F in (%proj_dir%) do set "env_name=%%~nF"
call :tolower env_name

set yaml_path=%script_dir%\environment.yaml
set env_path=%script_dir%\envs\%env_name%

set conda_cmd=conda env create -f %yaml_path% -p %env_path%

echo %conda_cmd%

call %conda_cmd%

goto :EOF

:: toupper & tolower; makes use of the fact that string replacement (via SET) is not case sensitive
:toupper
for %%L IN (^^ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) DO CALL SET "%1=%%%1:%%L=%%L%%%"
goto :EOF

:tolower
for %%L IN (^^ a b c d e f g h i j k l m n o p q r s t u v w x y z) DO CALL SET "%1=%%%1:%%L=%%L%%%"
goto :EOF
