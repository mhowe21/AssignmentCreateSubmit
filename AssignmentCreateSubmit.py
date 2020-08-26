try:
    import requests
except ModuleNotFoundError:
    print("attempting to install requests")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])


class InData():
    def __init__(self):
        self.instance = None
        self.token = None
        self.course = None
        self.assignments = None
        self.user = None
        self.fileID = None

    def canvasEnv(self):
        """
        Get the Canvas enviroment that is being targeted."""
        self.instance = input(
            "enter the canvas domain e.g canvas.instructure.com ")
        # remove spaces
        self.instance = self.instance.replace(" ", "")
        return self.instance

    def canvasToken(self):
        """
        Get the users Canvas REST token.
        """
        self.token = input("enter your canvas token ")
        # remove spaces
        self.token = self.token.replace(" ", "")
        return self.token

    def canvasCourse(self):
        """
        Get the course ID in canvas that is being targeted.
        """
        self.course = input("enter canvas course ID ")
        # remove spaces
        self.course = self.course.replace(" ", "")
        return self.course

    def canvasAssignments(self):
        """
        Get the number of assignments to be made
        """
        self.assignments = input("enter the number of assignments ")
        # remove spaces
        self.assignments = self.assignments.replace(" ", "")
        return self.assignments

    def canvasUser(self):
        """
        Get the Canvas user to submit the assignments as
        """
        self.user = input("enter the canvas user ID ")
        # remove spaces
        self.user = self.user.replace(" ", "")
        return self.user

    def canvasFile(self):
        """
        Get the ID of the File to Submit
        """
        self.fileID = input("Enter the file ID you would like to use ")
        # remove spaces
        self.fileID = self.fileID.replace(" ", "")
        return self.fileID


class APICalls:

    def __init__(self, token, instance, course, assignments, user, files):
        self.token = token
        self.instance = instance
        self.course = course
        self.assignments = int(assignments)
        self.user = user
        self.files = files
        self.assignmentList = []

    def makeAssignments(self):
        """
        Make the number of selected assignments. 
        In the specified course
        """

        for i in range(self.assignments):
            url = f"https://{self.instance}/api/v1/courses/{self.course}/assignments/"

            payload = {'assignment[name]': 'testingSubmission',
                       'assignment[submission_types][]': 'online_upload',
                       'assignment[points_possible]': '10',
                       'assignment[published]': 'True'}
            files = [

            ]
            headers = {
                'Authorization': f'Bearer {self.token}'

            }

            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files)

        print(response.text.encode('utf8'))

    def getCourseAssignments(self):
        """
        Get a list of all the assignments in the course. 
        """

        url = f"https://{self.instance}/api/v1/courses/{self.course}/assignments/"

        payload = {'per_page': '100'}
        files = [

        ]
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        while(url is not None):
            response = requests.request(
                "GET", url, headers=headers, data=payload, files=files)

            print(response.text.encode('utf8'))
            JData = response.json()

            for item in JData:
                self.assignmentList.append(item["id"])

            try:
                linkHeaders = response.links["next"]["url"]
                url = linkHeaders
            except KeyError:
                url = None

        return self.assignmentList

    def uploadFile(self):
        """
        Upload a file ID in Canvas to a selected set of assignments. 
        """

        for id in self.assignmentList:
            url = f"https://{self.instance}/api/v1/courses/{self.course}/assignments/{id}/submissions/"

            payload = {'submission[submission_type]': 'online_upload',
                       'submission[file_ids][]': f'{self.files}',
                       'as_user_id': f'{self.user}'}
            files = [

            ]
            headers = {
                'Authorization': f'Bearer {self.token}',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files)

            print(response.text.encode('utf8'))


def main():
    data = InData()
    token = data.canvasToken()
    instance = data.canvasEnv()
    course = data.canvasCourse()
    assignments = data.canvasAssignments()
    user = data.canvasUser()
    fileID = data.canvasFile()

    calls = APICalls(token, instance, course, assignments, user, fileID)
    print("making assignments...")
    calls.makeAssignments()
    print("done making assignments")
    print("gathering assignments...")
    calls.getCourseAssignments()
    print("done gathering assignments")
    print("Submitting file to assignment...")
    calls.uploadFile()
    print("Done...")


if __name__ == "__main__":
    main()
