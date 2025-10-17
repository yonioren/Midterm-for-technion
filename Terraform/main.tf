resource "aws_vpc" "jenkins_vpc" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "main"
  }
}

resource "aws_security_group" "jenkins-sg" {
  name        = "jenkins-sg"
  description = "Security group for Jenkins demo"
  vpc_id      = aws_vpc.jenkins_vpc.id

  # Allow SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name      = "jenkins-sg"
  }

}

resource "aws_subnet" "Jenkins_Subnet" {
  vpc_id     = aws_vpc.jenkins_vpc.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "Jenkins_Subnet"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.jenkins_vpc.id
}

resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.jenkins_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "rta" {
  subnet_id      = aws_subnet.Jenkins_Subnet.id
  route_table_id = aws_route_table.rt.id
}

# KEY
resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "KP" {
  key_name   = "MyKey"
  public_key = tls_private_key.key.public_key_openssh
}

# EC2 instance
resource "aws_instance" "app" {
  ami           = "ami-0341d95f75f311023"
  instance_type = "t3.medium"
  
  subnet_id                   = aws_subnet.Jenkins_Subnet.id
  vpc_security_group_ids      = [aws_security_group.jenkins-sg.id]
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              # Update system
              yum update -y
              
              # Install Docker
              yum install docker -y
              service docker start
              usermod -a -G docker ec2-user
              
              # Pull the image
              docker pull ${var.docker_image}
              
              # Run container and save output
              docker run --name python-app ${var.docker_image} bash -c "ls /ProjectPlanner/" > /home/ec2-user/app-output.txt 2>&1
              
              # Create a summary file
              echo "Container execution completed at $(date)" > /home/ec2-user/README.txt
              echo "Output saved to: /home/ec2-user/app-output.txt" >> /home/ec2-user/README.txt
              echo "View output: cat /home/ec2-user/app-output.txt" >> /home/ec2-user/README.txt
              
              # Fix permissions
              chown ec2-user:ec2-user /home/ec2-user/app-output.txt
              chown ec2-user:ec2-user /home/ec2-user/README.txt
              touch /tmp/finished_userdata
              EOF

  tags = {
    Name      = "jenkins-python-app"
  }

  provisioner "remote-exec" {
        inline = [
            "bash -c \"until test -f /tmp/finished_userdata &>/dev/null; do sleep 1; done; cat /home/ec2-user/README.txt; cat /home/ec2-user/app-output.txt; hostname\""
        ]
       connection {
            type        = "ssh"
            user        = "ec2-user"
            private_key = tls_private_key.key.private_key_pem
            host        = aws_instance.app.public_ip
       }
    }
}
