*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Go To Starting Page

*** Test Cases ***
Click Login Link
    Click  text=Login
    Login Page Should Be Open

Click Register Link
    Click  text=Register new user
    Register Page Should Be Open
