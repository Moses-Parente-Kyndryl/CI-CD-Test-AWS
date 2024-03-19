provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "opa_instance" {
  ami           = "ami-047869c10b5107b42"  # Replace with a valid AMI ID for your region
  instance_type = "t2.micro"

  tags = {
    Name = "OPA Instance"
  }
}
#Test_new_bundle2
