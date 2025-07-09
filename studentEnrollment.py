#!/usr/bin/env python
# coding: utf-8

# In[9]:


class main() :
    users={1:{"userName":"admin","fname":"admin","lname":"admin","email":"","pwd":"","city":"","state":"","zipcode":"","country":""}}
    nextUserID = 2
    learners = {}
    nextLearnerID = 1
    courses = {}
    nextCourseID = 1
    instructors = {}
    nextInstructorID = 1

    def listUsers(self):
        print("User List")
        for x,y in self.users.items():
            print("ID: "+str(x)+"\tName: "+y["fname"]+' '+y["lname"]+"\tEmail: "+y["email"]+"\tCity: "+y["city"]+'\tState: '+y["state"]+'\tZipCode: '+y["zipcode"]+'\tCountry: '+y["country"])

    def listLearners(self) :
        print('Learners')
        for k,v in self.learners.items() :
            for x,y in self.users.items() :
                if v == x :
                    print("Learner ID: "+str(k)+"\tUser ID: "+' '+str(x)+"\tName: "+y["fname"]+' '+y["lname"]+"\tEmail: "+y["email"]+"\tCity: "+y["city"]+'\tState: '+y["state"]+'\tZipCode: '+y["zipcode"]+'\tCountry: '+y["country"])
                else:
                    continue

    def listInstructors(self) :
        print('Instructors')
        for k,v in self.instructors.items() :
            for x,y in self.users.items() :
                if v == x :
                    print("Instructor ID: "+str(k)+"\tUser ID: "+' '+str(x)+"\tName: "+y["fname"]+' '+y["lname"]+"\tEmail: "+y["email"]+"\tCity: "+y["city"]+'\tState: '+y["state"]+'\tZipCode: '+y["zipcode"]+'\tCountry: '+y["country"])
                else:
                    continue

    def listCourses(self) :
        print('Courses')
        for k,v in self.courses.items() :
            print("Course ID: "+str(k)+"\tCourse Code: "+v["courseCode"]+"\tDescription: "+v["description"]+"\tStart Date: "+v["startDate"]+"\tEnd Date: "+v["endDate"])


# In[22]:


class users(main):
    uMenu = {1 : "Add New User", 2 : "List All Users", 3 : "Update User Email", 4 : "Update User Password", 
                     5 : "Delete User", 6 : "Return to main menu"}

    def __init__(self) :
        main.__init__(main)
        
    def userMenu(self,userID) :
        print('Option ID')
        
        for k in self.uMenu.keys() :
            print(str(k)+'\t'+self.uMenu[k])
        
        opt = int(input('Enter option number from choices above : \n\n'))
        
        if opt == 1 :
            r = self.addUser()
            return self.userMenu(userID)
        
        elif opt == 2 :
            self.listUsers()
            return self.userMenu(userID)

        elif opt == 3 :
            uID = int(input('Enter ID of user to update email : '))
            newEmail = self.validateEmail()
            email = self.checkEmailExists(newEmail)
            self.updateUser(uID,email=email)
            return self.userMenu(userID)

        elif opt == 4 :
            uID = int(input('Enter ID of user to update password, enter -1 to show list of all users : '))
            if uID == -1 :
                self.listUsers()
                uID = int(input('Enter ID of user to update password : '))
            pwd = self.enterPassword()
            self.updateUser(uID,pwd=pwd)
            return self.userMenu(userID)

        elif opt == 5 :
            u = int(input('Enter user ID to delete, Enter -1 to list all users : '))
            if u == -1 :
                self.listUsers()
                u = int(input('Enter user ID to delete'))
                self.delUser(u)
                return self.userMenu(userID)
            elif u == 1 :
                print('Deleting user ID 1, Admin user is not allowed')
                return self.userMenu(userID)
            else :
                self.delUser(u)
                return self.userMenu(userID)

        elif opt == 6 :
            return userID

        else :
            return self.userMenu(userID)
    
    def enterPassword(self) :
        pwd1 = input('Enter User\'s Password')
        pwd2 = input('Re-Enter User\'s Password')
        if pwd1 != pwd2 :
            return self.enterPassword()

        else :
            return pwd1
            
    def checkEmailExists(self,email) :
        for k in users.users.keys() :
            if main.users[k]["email"] == email :
                email = input('Email already in use. Please try another email address : ')
                return self.checkEmailExists(email)
            else :
                return email
    
    def setAdminPwd(self,email,pwd) :
        r1 = self.users[1]
        r1["email"]=email
        r1["pwd"]=pwd
        main.users[1].update(r1)
    
    def validateUser(self,email,pwd) :
        max_id = max(main.users)
        sorted_dict = dict(sorted(self.users.items()))
        for k in sorted_dict.keys() :
            
            if self.users[k]["email"] == email and pwd == self.users[k]["pwd"] :
                return k

            elif k != max_id :
                continue
            
            else :
                print ("No user found, please try again")
                email = input("Enter Email Address : ")
                pwd = input("Enter Password : ")
                return self.validateUser(email,pwd)
    
    def validateEmail(self) :
        email = input("Enter User Email Address : ")
        
        if '@' not in email or '.' not in email :
            print('Not a valid email address please try again')
            return self.validateEmail()

        else :
            return email
            
    
    def addUser(self) :
        email = self.validateEmail()
        sorted_users = dict(sorted(main.users.items()))
        max_user_id = max(sorted_users)
        email = self.checkEmailExists(email)
        uID = main.nextUserID
        main.nextUserID = main.nextUserID+1
        pwd = self.enterPassword()
        fname = input('User First Name')
        lname = input('User Last Name')
        dob = input('User Date of Birth')
        city = input('User City')
        state = input('User State')
        zipcode = input('User Zipcode')
        country = input('User Country')
        record = {uID : {"userName": fname.title()+' '+lname.title(), "fname" : fname.title(), "lname" : lname.title(), "email" : email, 
                                         "pwd": pwd, "dob" : dob, "city" : city.title(), "state": state.upper(), "zipcode" : zipcode, "country" : country.upper()}}
        main.users.update(record)
        return 'User Successfully Added'
    

    def delUser(self,userID) :
        del main.users[userID]
        return 'User Deleted'

    def updateUser(self,userID,**kwargs) :
        main.users[userID].update(kwargs)
        return 'User Updated'
     


# In[68]:


class courses(main) :

    cMenu = {1 : "Enter New Course", 2 : "List all Courses", 3 : "Delete Course", 4 : "Add Learner", 5: "Remove Learner", 
             6 : "List Learners", 7: "List Learners enrolled in Course", 8 : "Return to Main Menu"}

    def __init__(self) :
        main.__init__(main)

    def courseMenu(self,userID) :
        print('Option ID')
        for k in self.cMenu.keys() :
            print(str(k)+'\t'+self.cMenu[k])
        opt = int(input('Enter option number from choices above : \n\n'))
        
        if opt == 1 :
            self.addCourse(userID)
            return self.courseMenu(userID)
        
        elif opt == 2 :
            self.listCourses()
            return self.courseMenu(userID)

            
        elif opt == 3 :
            u = int(input('Enter Course ID to delete, Enter -1 to list all courses : '))
            if u == -1 :
                self.listCourses()
                u = int(input('Enter Course ID to delete : '))
                self.delCourses(u)
                return self.courseMenu(userID)
            
            else :
                self.delCourses(u)
                return self.courseMenu(userID)

        elif opt == 4 : 
            self.addLearnerC(userID)
            return self.courseMenu(userID)

        elif opt == 5 : 
            u = int(input('Enter Learner ID to delete, Enter -1 to list all learners : '))
            if u == -1 :
                self.listLearners()
                u = int(input('Enter Learner ID to delete, Enter -1 to list all learners : '))
                self.delLearnerC(u)
                return self.courseMenu(userID)
            
            else :
                self.delLearnerC(u)
                return self.courseMenu(userID)

        elif opt == 6 :
            self.listLearners()
            return self.courseMenu(userID)

        elif opt == 7 :
            self.listCourseLearners(userID)
            return self.courseMenu(userID)
        
        elif opt == 8 :
            return userID

        else :
            return self.courseMenu(userID)


    def delCourses(self,courseID) :
        del main.courses[courseID]
        print('Course Deleted')


    def addCourse(self,userID) :
        courseID = main.nextCourseID
        main.nextCourseID += 1
        print('Input Values')
        cID = input("Course Code : ")
        for k, v in main.courses.items() :
            #if v["courseID"] == cID :
            if v.get("courseCode",'zz') == cID :
                print("Course Already Exists\n")
                return userID
            
            else :
                continue
        cDesc = input('Course Description : ')
        cDept = input('Department : ')
        cStartDate = input('Start Date : ')
        cEndDate = input('End Date : ')
        max_learners = int(input('Max Learners : '))
        creditHours = float(input('Credit Hours : '))
        record = {courseID : {"courseCode" : cID,"description" : cDesc, "department" : cDept, "instructors" : [], "learners" : [], "startDate" : cStartDate, 
                              "endDate" : cEndDate, "max_learners" : max_learners, "creditHours" : creditHours}}
        
        main.courses.update(record)
        print('Course Successfully Added')
        return userID
    
    def delLearnerC(self,learnerID) :
        del main.learners[learnerID]
        return 'Learner Deleted'

    def addLearnerC(self,userID) :
        learnerID = main.nextLearnerID
        main.nextLearnerID += 1
        uID = int(input("Enter User ID to create new learner or enter -1 to list all users : "))
        
        if uID == -1 :
            self.listUsers()
            uID = int(input("Enter User ID to create new learner : "))
        
        for k, v in main.learners.items() :
            if v == uID :
                print("Learner Already Exists\n")
                return userID
            
            else :
                continue
                
        record = {learnerID : userID}
        main.learners.update(record)
        print('Learner Successfully Added')
        return userID

    def listCourseLearners(self,userID) :
        cID = int(input('Enter Course ID or enter -1 to list all courses : '))
        if cID == -1 :
            self.listCourses()
            cID = int(input('Enter Course ID : '))
            print('Learner ID\tLearner Name') 
            for i in self.courses[cID]["learners"] :
                print(str(i)+'\t\t'+self.users[self.learners[i]]["userName"])
            return userID
            
           
        else :
            for i in self.courses[cID]["learners"] :
                print(str(i)+'\t\t'+self.users[self.learners[i]]["userName"])
            return userID
                


# In[69]:


class learners(users,courses,main) :

    lMenu = {1 : "Enter New Learner", 2 : "List Learners", 3 : "Delete Learner", 
             4: "List All Courses", 5 : "Enroll Learner in Course", 6 : "Remove Learner From Course", 
             7 : "Show Learner\'s courses", 8 : "Return to Main menu"}
    
    def __init__(self) :
        users.__init__(users)
        courses.__init__(courses)
        main.__init__(main)


    def learnerMenu(self,userID) :
        print('Option ID')
        
        for k in self.lMenu.keys() :
            print(str(k)+'\t'+self.lMenu[k])
        
        opt = int(input('Enter option number from choices above : \n\n'))
        
        if opt == 1 :
            self.addLearner(userID)
            return self.learnerMenu(userID)
        
        elif opt == 2 :
            self.listLearners()
            return self.learnerMenu(userID)

            
        elif opt == 3 :
            u = int(input('Enter Learner ID to delete, Enter -1 to list all learners : '))
            if u == -1 :
                self.listLearners()
                u = int(input('Enter Learner ID to delete, Enter -1 to list all learners : '))
                self.delLearner(u)
                return self.learnerMenu(userID)
            
            else :
                self.delLearner(u)
                return self.learnerMenu(userID)

        elif opt == 4 :
            print(self.listCourses())
            return self.learnerMenu(userID)

        elif opt == 5 :
            lID = int(input('Enter Learner ID or enter -1 to see a list all learners : '))
            
            if lID == -1 :
                self.listLearners()
                lID = int(input('Enter Learner ID to add Learner : '))
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.enrollLearner(userID,cID,lID)

            else :
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.enrollLearner(userID,cID,lID)

                else :
                    self.enrollLearner(userID,cID,lID)
            return self.learnerMenu(userID)

        elif opt == 6 :
            lID = int(input('Enter Learner ID or enter -1 to see a list all learners : '))
            
            if lID == -1 :
                self.listLearners()
                lID = int(input('Enter Learner ID to remove : '))
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.unEnrollLearner(userID,cID,lID)

            else :
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.unEnrollLearner(userID,cID,lID)

                else :
                    self.unEnrollLearner(userID,cID,lID)
            return self.learnerMenu(userID)

        elif opt == 7 :
            self.listLearnerCourses()
            self.learnerMenu(userID)
        
        elif opt == 8 :
            return userID

        else :
            return self.learnerMenu(userID)
            

    def delLearner(self,userID) :
        u = int(userID)
        del main.learners[u]
        return 'Learner Deleted'

    def addLearner(self,userID) :
        learnerID = main.nextLearnerID
        main.nextLearnerID += 1
        uID = int(input("Enter User ID to create new learner or enter -1 to list all users : "))
        
        if uID == -1 :
            self.listUsers()
            uID = int(input("Enter User ID to create new learner : "))
        
        for k, v in main.learners.items() :
            if v == uID :
                print("Learner Already Exists\n")
                return userID
            
            else :
                continue

        record = {learnerID : uID}
        main.learners.update(record)
        print('Learner Successfully Added')
        return userID

    def enrollLearner(self,userID,cID,lID) :
        main.courses[cID]["learners"].append(lID)
        return userID

    def unEnrollLearner(self,userID,cID,lID) :
        main.courses[cID]["learners"].remove(lID)
        return userID

    def listLearnerCourses(self) :
        lID = int(input('Enter Learner ID or enter -1 to see list all learners : '))
        if lID == -1 :
            self.listLearners()
            lID = int(input('Enter Learner ID : '))
        print('Enrolled Courses')
        for x,y in self.courses.items() :
            if lID in y.get("learners",-99) :
                print("Course ID: "+' '+str(x)+"\tDescription: "+y["description"]+"\tStart Date: "+y["startDate"]+"\tEnd Date: "+y["endDate"])
                
            else:
                continue


# In[70]:


class instructors(users,courses,main) :

    iMenu = {1 : "Enter New Instructor", 2 : "List Instructors", 3 : "Delete Instructor", 4: "List All Courses", 
                           5 : "Assign instructor to Course", 6 : "Un-assign Instructor From Course", 7 : "Return to Main menu"}
    
    def __init__(self) :
        users.__init__(users)
        courses.__init__(courses)
        main.__init__(main)


    def instructorMenu(self,userID) :
        print('Option ID')
        
        for k in self.iMenu.keys() :
            print(str(k)+'\t'+self.iMenu[k])
        
        opt = int(input('Enter option number from choices above : \n\n'))
        
        if opt == 1 :
            self.addInstructor(userID)
            return self.instructorMenu(userID)
        
        elif opt == 2 :
            self.listInstructors()
            return self.instructorMenu(userID)

            
        elif opt == 3 :
            u = int(input('Enter instructor ID to delete, Enter -1 to list all instructors : '))
            if u == -1 :
                self.listInstructors()
                u = int(input('Enter instructor ID to delete, Enter -1 to list all instructors : '))
                self.delInstructor(u)
                return self.instructorMenu(userID)
            
            else :
                self.delInstructor(u)
                return self.instructorMenu(userID)

        elif opt == 4 :
            self.listCourses()
            return self.instructorMenu(userID)

        elif opt == 5 :
            iID = int(input('Enter instructor ID or enter -1 to see a list all instructors : '))
            
            if iID == -1 :
                self.listInstructors()
                iID = int(input('Enter instructor ID to assign instructor : '))
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.assignInstructor(userID,cID,iID)

            else :
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.assignInstructor(userID,cID,iID)

                else :
                    self.assignInstructor(userID,cID,iID)

        elif opt == 6 :
            iID = int(input('Enter instructor ID or enter -1 to see a list all instructors : '))
            
            if iID == -1 :
                self.listInstructors()
                iID = int(input('Enter instructor ID to remove : '))
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.unAssignInstructor(userID,cID,iID)

            else :
                cID = int(input('Enter Course ID or enter -1 to list all courses : '))
                
                if cID == -1 :
                    self.listCourses()
                    cID = int(input('Enter Course ID : '))
                    self.unAssignInstructor(userID,cID,iID)

                else :
                    self.unAssignInstructor(userID,cID,iID)

            return self.instructorMenu(userID)

        elif opt == 7 :
            return userID

        else :
            return self.instructorMenu(userID)
            

    def delInstructor(self,userID) :
        u = int(userID)
        del main.instructors[u]
        return userID

    def addInstructor(self,userID) :
        instructorID = main.nextInstructorID
        main.nextInstructorID += 1
        uID = int(input("Enter User ID to create new instructor or enter -1 to list all users : "))
        
        if uID == -1 :
            self.listUsers()
            uID = int(input("Enter User ID to create new instructor : "))
        
        for k, v in main.instructors.items() :
            if v == uID :
                print("Instructor Already Exists\n")
                return userID
            
            else :
                continue

        record = {instructorID : uID}
        main.instructors.update(record)
        print('Instructor Successfully Added')
        return userID

    def assignInstructor(self,userID,cID,iID) :
        main.courses[cID]["instructors"].append(iID)
        return userID

    def unAssignInstructor(self,userID,cID,iID) :
        main.courses[cID]["instructors"].remove(iID)
        return userID


# In[71]:


class enrollment(instructors,learners) :
    eMenu = {1 : "User Options", 2 : "Learner Options", 3 : "Instructor Options", 4 : "Course Options", 99 : "Exit Enrollment" }
    
    
    def enrollmentMenu(self,userID) :
        print('Option ID')
        for k in self.eMenu.keys() :
            print(str(k)+'\t'+self.eMenu[k])
        
        opt = int(input('Enter option number from choices above : \n\n'))

        if opt == 1 :
            userID = self.userMenu(userID)
            return self.enrollmentMenu(userID)

        elif opt == 2 :
            userID = self.learnerMenu(userID)
            return self.enrollmentMenu(userID)

        elif opt == 3 :
            userID = self.instructorMenu(userID)
            return self.enrollmentMenu(userID)

        elif opt == 4 :
            userID = self.courseMenu(userID)
            return self.enrollmentMenu(userID)

        elif opt == 99 :
            print('Bye-Bye')

        else :
            return self.enrollmentMenu(userID)


    


# In[72]:


enrollment = enrollment()


# In[ ]:


if len(enrollment.users[1]["pwd"]) == 0 :
    email = input("Please enter your admin user's email address")
    pwd = enrollment.enterPassword()
    enrollment.setAdminPwd(email,pwd)
            

print("Login")
uEmail = input("Enter your email address")
pwd = input("Enter your password")
userID = enrollment.validateUser(uEmail,pwd)

enrollment.enrollmentMenu(userID) 


# In[ ]:




