TYPE T_StaeubliRobot :
    STRUCT
        Status : T_Status ;
        Command : T_Command ;
        CommandInterface : T_CommandInterface ;
    END_STRUCT
END_TYPE


TYPE T_Status:
    STRUCT
        Initialized: BOOL ; (* True = The library is initialized *)
        Online: BOOL ; (* True = robot can receive commands *)
        ErrorPending: BOOL ; (* True = an error is pending *)
        IsMoving: BOOL ; (* True = robot is moving *)
        EStopActive: BOOL ; (* True = E-stop is pending *)
        DummyPlug: BOOL ; (* True = staubli teach pendant replaced by dummy
        plug *)
        ExternalMcp_Wms: BOOL ; (* True = Robot is properly configured to use both
        user- supplied WMS and Teach Pendant. *)
        ActualSpeed: REAL ; (* Cartesian speed of the current TCP *)
        ActualOverride: REAL ; (* Current override value [0.01 .. 100] *)
        ActualErrorNumber: UINT ; (* Total number of pending errors in robot *)
        ActualOperationMode: UINT ; (* Actual working mode 0= invalid , 1=manu,
        3=Auto, 4=remote(extaut) *)
        ActualErrorID: T_PendingErrors ; (* List of pending error on server side *)
        CartesianPos: T_CartesianPos ; (* Current cartesian position *)
        JointPos: T_JointPos ; (* Current joint position *)
        ActualCoordSystem: UINT ; (* Number of the user frame in which the position of
        the Tool Center Point is reported *)
        ActualTool: UINT ; (* Number of the Tool Center Point for which the
        position is reported *)
        RobotStateMachine: UINT ; (* State Machine of the robot *)
        MovementID: INT ; (* Identifier of motion currently executed *)
        MovementProgress: INT ; (* Percentage of actual movement that has been
        completed *)
        RobotModel: INT (* Robot model connected to controller *)
        ControllerModel: UINT ; (* Staubli controller 8=CS8C / 9=CS9 *)
        CS9Safety: T_CS9SftyFbk ; (* CS9 Only - Safety features *)
        Heartbeat: UINT ;
        ServerMajorVersion: UINT ; (* Major version of unival PLC server *)
        ServerMinorVersion: UINT ; (* Minor version of unival PLC server *)
        ServerEdit: UINT ; (* Edit of the uniVAL plc server *)
        ClientMajorVersion: UINT ; (* Major version of unival PLC client library *)
        ClientMinorVersion: UINT ; (* Minor version of unival PLC client library *)
        ClientEdit: UINT ; (* Edit of the unival PLC client library *)
    END_STRUCT
END_TYPE

TYPE T_Command :
    STRUCT
        EnableVerbose : BOOL ; (* TRUE=Enable tracing activity of the server. It is
        strongly recommended to enable trace for debugging
        purpose only. Starting with FALSE *)
        OverrideCmd : UINT ; (* Commanded Override [1..100] (monitor speed) Starting
        with 0 *)
        OperationModeCmd : UINT ; (* Commanded operation mode 0= invalid , 1= Manu,
        3=Auto, 4 remote(extAut) *)
        ToolCmd : UINT ; (* Select the Tool used for movement. Starting with 0*)
        CoordSystemCmd : UINT ; (* Select the coordinate system used for movement.
        Starting with 0 *)
        CS9Safety : T_CS9SftyCmd ; (* CS9 Only - Safety features *)
        LifebitPeriod : TIME ; (* Select the period of the internal lifebit
        (100ms<Period<1000ms) . starting with t#200ms *)
    END_STRUCT
END_TYPE

