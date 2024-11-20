@Echo Off
REM ��������� ����� ������ � �������, ����� ������ ������ ���������� ���������� �������.
chcp 1251
Echo ������� ������� ��������: 1251

SetLocal EnableDelayedExpansion
REM �������� ����� ������������ ������������ ����������.

REM ������������� ���������� � ������� � ������ ����� ���������.
Set "Process1Name=YPlateVision.exe"
Set "Process1Path=C:\�������\Rec"
Set "Process2Name=Checker2.2a.exe"
Set "Process2Path=C:\�������"

Echo ���� � Process1: "%Process1Path%"
Echo ��� Process1: "%Process1Name%"
Echo ���� � Process2: "%Process2Path%"
Echo ��� Process2: "%Process2Name%"

REM ��������� ����������� ���� ��� ����������� � ������� ���������.
:loop
REM ���������, ������� �� Process1.
TaskList /FI "ImageName EQ %Process1Name%" | Find /I "%Process1Name%" > Nul
REM ���� Process1 �� �������, �� �������� ��� ���������.
If !ErrorLevel! NEQ 0 (
    Echo ������� ������� %Process1Name% �� %Process1Path%
    If Exist "%Process1Path%\%Process1Name%" (
        Pushd "%Process1Path%"
        Start "" "%Process1Path%\%Process1Name%"
        Popd
        Echo %Process1Name% �������.
    ) Else (
        Echo ���� %Process1Name% �� ������ � %Process1Path%.
    )
) Else (
    Echo Process1 ��� �������.
)

REM ���������, ������� �� Process2.
TaskList /FI "ImageName EQ %Process2Name%" | Find /I "%Process2Name%" > Nul
REM ���� Process2 �� �������, �� �������� ��� ���������.
If !ErrorLevel! NEQ 0 (
    Echo ������� ������� %Process2Name% �� %Process2Path%
    If Exist "%Process2Path%\%Process2Name%" (
        Pushd "%Process2Path%"
        Start "" "%Process2Path%\%Process2Name%"
        Popd
        Echo %Process2Name% �������.
    ) Else (
        Echo ���� %Process2Name% �� ������ � %Process2Path%.
    )
) Else (
    Echo Process2 ��� �������.
)

REM ������������� �������� ����� ��������� ��������� �����.
timeout /T 10
Echo ����� �������� 10 ������ ���������, ����������� ������.

REM ������� � ��������� �������� �����.
goto loop
