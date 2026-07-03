;; Auto-generated. Do not edit!


(when (boundp 'mycobot_communication::MycobotPumpStatus)
  (if (not (find-package "MYCOBOT_COMMUNICATION"))
    (make-package "MYCOBOT_COMMUNICATION"))
  (shadow 'MycobotPumpStatus (find-package "MYCOBOT_COMMUNICATION")))
(unless (find-package "MYCOBOT_COMMUNICATION::MYCOBOTPUMPSTATUS")
  (make-package "MYCOBOT_COMMUNICATION::MYCOBOTPUMPSTATUS"))

(in-package "ROS")
;;//! \htmlinclude MycobotPumpStatus.msg.html


(defclass mycobot_communication::MycobotPumpStatus
  :super ros::object
  :slots (_Status ))

(defmethod mycobot_communication::MycobotPumpStatus
  (:init
   (&key
    ((:Status __Status) nil)
    )
   (send-super :init)
   (setq _Status __Status)
   self)
  (:Status
   (&optional __Status)
   (if __Status (setq _Status __Status)) _Status)
  (:serialization-length
   ()
   (+
    ;; bool _Status
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _Status
       (if _Status (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _Status
     (setq _Status (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get mycobot_communication::MycobotPumpStatus :md5sum-) "513e93c68ef2f26ff494445b932bb052")
(setf (get mycobot_communication::MycobotPumpStatus :datatype-) "mycobot_communication/MycobotPumpStatus")
(setf (get mycobot_communication::MycobotPumpStatus :definition-)
      "bool Status

")



(provide :mycobot_communication/MycobotPumpStatus "513e93c68ef2f26ff494445b932bb052")


