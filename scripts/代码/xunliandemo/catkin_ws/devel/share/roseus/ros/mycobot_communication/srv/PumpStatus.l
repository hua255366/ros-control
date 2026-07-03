;; Auto-generated. Do not edit!


(when (boundp 'mycobot_communication::PumpStatus)
  (if (not (find-package "MYCOBOT_COMMUNICATION"))
    (make-package "MYCOBOT_COMMUNICATION"))
  (shadow 'PumpStatus (find-package "MYCOBOT_COMMUNICATION")))
(unless (find-package "MYCOBOT_COMMUNICATION::PUMPSTATUS")
  (make-package "MYCOBOT_COMMUNICATION::PUMPSTATUS"))
(unless (find-package "MYCOBOT_COMMUNICATION::PUMPSTATUSREQUEST")
  (make-package "MYCOBOT_COMMUNICATION::PUMPSTATUSREQUEST"))
(unless (find-package "MYCOBOT_COMMUNICATION::PUMPSTATUSRESPONSE")
  (make-package "MYCOBOT_COMMUNICATION::PUMPSTATUSRESPONSE"))

(in-package "ROS")





(defclass mycobot_communication::PumpStatusRequest
  :super ros::object
  :slots (_Status ))

(defmethod mycobot_communication::PumpStatusRequest
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

(defclass mycobot_communication::PumpStatusResponse
  :super ros::object
  :slots (_Flag ))

(defmethod mycobot_communication::PumpStatusResponse
  (:init
   (&key
    ((:Flag __Flag) nil)
    )
   (send-super :init)
   (setq _Flag __Flag)
   self)
  (:Flag
   (&optional __Flag)
   (if __Flag (setq _Flag __Flag)) _Flag)
  (:serialization-length
   ()
   (+
    ;; bool _Flag
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _Flag
       (if _Flag (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _Flag
     (setq _Flag (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass mycobot_communication::PumpStatus
  :super ros::object
  :slots ())

(setf (get mycobot_communication::PumpStatus :md5sum-) "c57caedf4aafd0b59704d2f3b16e0f35")
(setf (get mycobot_communication::PumpStatus :datatype-) "mycobot_communication/PumpStatus")
(setf (get mycobot_communication::PumpStatus :request) mycobot_communication::PumpStatusRequest)
(setf (get mycobot_communication::PumpStatus :response) mycobot_communication::PumpStatusResponse)

(defmethod mycobot_communication::PumpStatusRequest
  (:response () (instance mycobot_communication::PumpStatusResponse :init)))

(setf (get mycobot_communication::PumpStatusRequest :md5sum-) "c57caedf4aafd0b59704d2f3b16e0f35")
(setf (get mycobot_communication::PumpStatusRequest :datatype-) "mycobot_communication/PumpStatusRequest")
(setf (get mycobot_communication::PumpStatusRequest :definition-)
      "bool Status

---

bool Flag
")

(setf (get mycobot_communication::PumpStatusResponse :md5sum-) "c57caedf4aafd0b59704d2f3b16e0f35")
(setf (get mycobot_communication::PumpStatusResponse :datatype-) "mycobot_communication/PumpStatusResponse")
(setf (get mycobot_communication::PumpStatusResponse :definition-)
      "bool Status

---

bool Flag
")



(provide :mycobot_communication/PumpStatus "c57caedf4aafd0b59704d2f3b16e0f35")


