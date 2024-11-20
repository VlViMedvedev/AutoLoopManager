@Echo Off
chcp 1251
Echo Текущая кодовая страница: 1251

SetLocal EnableDelayedExpansion

Set "Process1Name=YPlateVision.exe"
Set "Process1Path=D:\KDV Agro IT\(3) Весовые\Распознование"

:loop
TaskList /FI "ImageName EQ %Process1Name%" | Find /I "%Process1Name%" > Nul
If !ErrorLevel! NEQ 0 (
    If Exist "%Process1Path%\%Process1Name%" (
        Pushd "%Process1Path%"
        Start "" "%Process1Name%"
        Popd
    ) Else (
        Echo Файл %Process1Name% не найден в "%Process1Path%".
    )
)

timeout /T 10
goto loop
