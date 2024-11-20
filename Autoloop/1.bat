@Echo Off
REM Отключаем вывод команд в консоль, чтобы видеть только результаты выполнения скрипта.
chcp 1251
Echo Текущая кодовая страница: 1251

SetLocal EnableDelayedExpansion
REM Включаем режим задержанного развёртывания переменных.

REM Устанавливаем переменные с именами и путями наших процессов.
Set "Process1Name=YPlateVision.exe"
Set "Process1Path=C:\Утилиты\Rec"
Set "Process2Name=Checker2.2a.exe"
Set "Process2Path=C:\Утилиты"

Echo Путь к Process1: "%Process1Path%"
Echo Имя Process1: "%Process1Name%"
Echo Путь к Process2: "%Process2Path%"
Echo Имя Process2: "%Process2Name%"

REM Запускаем бесконечный цикл для мониторинга и запуска процессов.
:loop
REM Проверяем, запущен ли Process1.
TaskList /FI "ImageName EQ %Process1Name%" | Find /I "%Process1Name%" > Nul
REM Если Process1 не запущен, то пытаемся его запустить.
If !ErrorLevel! NEQ 0 (
    Echo Попытка запуска %Process1Name% из %Process1Path%
    If Exist "%Process1Path%\%Process1Name%" (
        Pushd "%Process1Path%"
        Start "" "%Process1Path%\%Process1Name%"
        Popd
        Echo %Process1Name% запущен.
    ) Else (
        Echo Файл %Process1Name% не найден в %Process1Path%.
    )
) Else (
    Echo Process1 уже запущен.
)

REM Проверяем, запущен ли Process2.
TaskList /FI "ImageName EQ %Process2Name%" | Find /I "%Process2Name%" > Nul
REM Если Process2 не запущен, то пытаемся его запустить.
If !ErrorLevel! NEQ 0 (
    Echo Попытка запуска %Process2Name% из %Process2Path%
    If Exist "%Process2Path%\%Process2Name%" (
        Pushd "%Process2Path%"
        Start "" "%Process2Path%\%Process2Name%"
        Popd
        Echo %Process2Name% запущен.
    ) Else (
        Echo Файл %Process2Name% не найден в %Process2Path%.
    )
) Else (
    Echo Process2 уже запущен.
)

REM Устанавливаем задержку перед следующей итерацией цикла.
timeout /T 10
Echo Время ожидания 10 секунд завершено, продолжение работы.

REM Переход к следующей итерации цикла.
goto loop
