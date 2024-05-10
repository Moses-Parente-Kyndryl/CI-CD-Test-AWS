provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "opa_instance" {
  ami           = "ami-047869c10b5107b42"  
  instance_type = "t2.micro"

  tags = {
   ## Name = "OPA Instance"
  }
}
#Test_new_bundle_10000111
#networktest
#pytests1
