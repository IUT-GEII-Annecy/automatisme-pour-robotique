TYPE TCtrlStatusGroup
    STRUCT
        m_xEnable : BOOL ;
        m_xBusy : BOOL ;
        m_xDone : BOOL ;
        m_xError : BOOL ;
        m_udiErrorID : UDINT ;
        m_xTimeOut : BOOL ;
    END_STRUCT
END_TYPE