; Auto-generated. Do not edit!


(cl:in-package mycobot_communication-msg)


;//! \htmlinclude MycobotPumpStatus.msg.html

(cl:defclass <MycobotPumpStatus> (roslisp-msg-protocol:ros-message)
  ((Status
    :reader Status
    :initarg :Status
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass MycobotPumpStatus (<MycobotPumpStatus>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MycobotPumpStatus>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MycobotPumpStatus)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name mycobot_communication-msg:<MycobotPumpStatus> is deprecated: use mycobot_communication-msg:MycobotPumpStatus instead.")))

(cl:ensure-generic-function 'Status-val :lambda-list '(m))
(cl:defmethod Status-val ((m <MycobotPumpStatus>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader mycobot_communication-msg:Status-val is deprecated.  Use mycobot_communication-msg:Status instead.")
  (Status m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MycobotPumpStatus>) ostream)
  "Serializes a message object of type '<MycobotPumpStatus>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'Status) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MycobotPumpStatus>) istream)
  "Deserializes a message object of type '<MycobotPumpStatus>"
    (cl:setf (cl:slot-value msg 'Status) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MycobotPumpStatus>)))
  "Returns string type for a message object of type '<MycobotPumpStatus>"
  "mycobot_communication/MycobotPumpStatus")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MycobotPumpStatus)))
  "Returns string type for a message object of type 'MycobotPumpStatus"
  "mycobot_communication/MycobotPumpStatus")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MycobotPumpStatus>)))
  "Returns md5sum for a message object of type '<MycobotPumpStatus>"
  "513e93c68ef2f26ff494445b932bb052")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MycobotPumpStatus)))
  "Returns md5sum for a message object of type 'MycobotPumpStatus"
  "513e93c68ef2f26ff494445b932bb052")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MycobotPumpStatus>)))
  "Returns full string definition for message of type '<MycobotPumpStatus>"
  (cl:format cl:nil "bool Status~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MycobotPumpStatus)))
  "Returns full string definition for message of type 'MycobotPumpStatus"
  (cl:format cl:nil "bool Status~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MycobotPumpStatus>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MycobotPumpStatus>))
  "Converts a ROS message object to a list"
  (cl:list 'MycobotPumpStatus
    (cl:cons ':Status (Status msg))
))
