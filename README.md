# Email Collection Architecture diagram

![banner](https://github.com/BharatKatyal/S3-Apigateway-SES/blob/main/github_doc_images/Architecture_diagram.png?raw=true)    

## This is a serverless component consisting of:

an Api Gateway with a POST /submit endpoint, that requires two parameters:
- `first_name`, a string, that represents the first name of the user, 
- `email`, a string representing the email address of the user which will receive

a Lambda will store the user's first name and email address in a Dynamo DB table referenced in the SAM Template (template.yaml) The Table should be `${AWS::StackName}-UserDataTable`. The function will then use SES(Simple Email Service)  to send an email out to the user which includes the first name of the user. 


The purpose of this sam template is meant to be for something like a landing page or a popup that may collect a users email then send a message. 

### Below is an example POST

#### Postman Test 

`{
    "first_name": "postman",
    "email": "postman@example.com"
}`




#### Lambda Event Json

`{
    "body": "{\"first_name\":\"Lambda\",\"email\":\"hello@lambda.com\"}"
}`

# Deployment Parameters
This component has two CloudFormation deployment parameters:

- `SES_SOURCE_EMAIL`, a required parameter, represents the email sender. Must be an SES verified email within the region of deployment, you can change the region on the template by modifying the `SES_REGION` reference. If you attempt to send email using a non-verified address or domain, the operation results in an "Email address not verified" error.

- `Cors AllowOrigin`, an optional parameter, where you can restrict access to only specified domains.



# Deployment How to 
1. `git clone https://github.com/BharatKatyal/S3-Apigateway-SES.git`
2. CD into the folder by running `cd S3-Apigateway-SES`
3. in the template.yaml Edit the following
- On Line 75 Edit Replace the `<ENTER_VERIFIED_EMAIL>`with your verified email on SES.  It should look similar to `SES_SOURCE_EMAIL: BK@live.com`

4. in your terminal type `sam build`
5. Then type `sam deploy` You may need to type `sam deploy --guided`

Once deployed you should see this in your terminal 

![banner](https://github.com/BharatKatyal/S3-Apigateway-SES/blob/main/github_doc_images/after_sam_deploy.png?raw=true) 


# Testing How to test
1. Copy the endpoint and hop into postman and do a post request 

`{
    "first_name": "postman",
    "email": "postman@example.com"
}`



If successful you should see this message in Postman followed by an email (If you do not see an email and you see this message check your junk folder)
`"Data submitted successfully. An email has been sent to your provided email address."`
![banner](https://github.com/BharatKatyal/S3-Apigateway-SES/blob/main/github_doc_images/postrequest.png?raw=true) 
Trouble Shooting

If you get the following error 
`"Error: An error occurred (MessageRejected) when calling the SendEmail operation: Email address is not verified. The following identities failed the check in region US-EAST-1: postman@example.com"`
- Verify that the email you entered is verified in SES in the deployment region 

if you get this error
`"Error: An error occurred (InvalidParameterValue) when calling the SendEmail operation: Missing final '@domain'"` Recheck step 3 to make sure you have inputted an email address

# Testing with Static Website

You may have noticed an S3 Bucket in the Template along with an index.html - Although this is optional you can add this endpoint to a static website.

To do so do the following
Update: Line 10 in the HTML file and update the endpoint 
![banner](https://github.com/BharatKatyal/S3-Apigateway-SES/blob/main/github_doc_images/html_update.png?raw=true) 

Go ahead and open the html file locally or on S3 and input the data. You should see the following screen when successful 

![banner](https://github.com/BharatKatyal/S3-Apigateway-SES/blob/main/github_doc_images/html_post.png?raw=true) 

# Additional Information for Production
1. You should modify the dynamo table ProvisionedThroughput referenced in the template.yaml configurations to match your use case. 
     ` ProvisionedThroughput:
        ReadCapacityUnits: 1
        WriteCapacityUnits: 1`

2. Modify the Lambda Policy to use case.
     ` Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UserDataTable`

3. Update CORS
 `AllowOrigin: "'*'"` # Replace with your domain in production
