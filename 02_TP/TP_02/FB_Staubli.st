FUNCTION_BLOCK VAL_ReadAxesGroup
    VAR_INPUT
        Enable : BOOL ; (* TRUE : contents of the FB is executed *)
    END_VAR
    VAR_IN_OUT
        AxesGroup : T_StaeubliRobot ; (* Data block for a robot *)
        IN : T_FromRobot ;
    END_VAR
    VAR_OUTPUT
        Error : BOOL ; (* set when function block has terminated with error *)
        ErrorID : UDINT ; (* error code *)
        Timeout : BOOL ; (* set when a timeout is detected *)
    END_VAR




    
FUNCTION_BLOCK VAL_WriteAxesGroup
    VAR_INPUT
        Enable : BOOL ; (TRUE : contents of the FB is executed *)
    END_VAR
    VAR_IN_OUT
        AxesGroup : T_StaeubliRobot ; (* Data block for a robot *)
    END_VAR
    VAR_OUTPUT
        Error : BOOL ; (* set when function block has terminated with error *)
        ErrorID : UDINT ; (* error code *)
        OUT : T_ToRobot ;
        Timeout : BOOL ; (* set when a timeout is detected *)
    END_VAR
