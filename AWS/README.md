# AWS

Ahhhh... Ze Claud...

One cloudformation yaml has all the code that we need.

It will build:
* 1 X VPC
* 2 X Public subnets (in different AZs)
  * 1 X Internet GW for access from the internet
  * Appropriate routing
* 2 X Private subnets (in different AZs)
  * 2 X Nat GWs with public IPs for access of the instances to the image in ECR
  * Appropriate routing
* Security groups:
  * Access from the internet to the LB in port web
  * Access from the LB to the app running instances in port 8666
* HA
  * Launch template:
    * EC2 instances which will
      * Use `yum` to set a docker env
      * Pull the image from ECR
      * Run the application in port 8666
    * IAM profile that will allow pulling from ECR (duhhhhh)
  * Scaling Group
    * 1 instance per subnet. Not more. Not less. 2 will do.
    * Associate with the Target Group
  * Load Balancer + Listener + Target Group
    * Listen in HTTP/80
    * Forward to HTTP/8666 of the Target Group
    * Stickiness!!!! 1 hour sticky sessions
      * Next version will have a DB to eliminate this section.
      * Eli did mention not to worry about it but I still do.

## Mandatory parameters

* ECR Image URL
* AMI ID

## Output

The URL. Everything else is ready by the time the deployment is done
