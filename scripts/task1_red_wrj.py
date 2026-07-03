###############################
    
    angles = [-80.69, 48, -90, 48, 5.97, -47.48]

    mc.send_angles(angles, 65)

    time.sleep(4)




    target_angles = [-80.69, -20, -45, 68, 5.97, -47.48]



    while angles[1] != target_angles[1] or angles[2] != target_angles[2] or angles[3] != target_angles[3]:

        if angles[1] > target_angles[1]:

            angles[1] -= 4

        elif angles[1] < target_angles[1]:

            angles[1] += 4



        if angles[2] > target_angles[2]:

            angles[2] -= 5

        elif angles[2] < target_angles[2]:

            angles[2] += 5



        if angles[3] < target_angles[3]:

            angles[3] += 4

        elif angles[3] > target_angles[3]:

            angles[3] -= 4



        mc.send_angles(angles, 65)

        time.sleep(1)



        



###############################