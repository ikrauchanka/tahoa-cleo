package main

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
	// "github.com/pquerna/termchalk/prettytable"
	"github.com/olekukonko/tablewriter"
	"os"
	"strconv"
	"strings"
)

func getPrice(InstanceType string) float64 {
	price := map[string]float64{
		"cc2.8xlarge": 1460.000,
		"cg1.4xlarge": 1533.000,
		"t2.nano":     4.745,
		"t2.micro":    9.490,
		"t2.small":    18.980,
		"t2.medium":   37.960,
		"t2.large":    75.920,
		"m4.large":    87.600,
		"m4.xlarge":   174.470,
		"m4.2xlarge":  349.670,
		"m4.4xlarge":  699.340,
		"m4.10xlarge": 1747.620,
		"c4.large":    76.650,
		"c4.xlarge":   152.570,
		"c4.2xlarge":  305.870,
		"c4.4xlarge":  611.740,
		"c4.8xlarge":  1222.750,
		"g2.2xlarge":  474.500,
		"g2.8xlarge":  1898.000,
		"r3.large":    121.180,
		"r3.xlarge":   243.090,
		"r3.2xlarge":  485.450,
		"r3.4xlarge":  970.900,
		"r3.8xlarge":  1941.800,
		"i2.xlarge":   622.690,
		"i2.2xlarge":  1244.650,
		"i2.4xlarge":  2489.300,
		"i2.8xlarge":  4978.600,
		"d2.xlarge":   503.700,
		"d2.2xlarge":  1007.400,
		"d2.4xlarge":  2014.800,
		"d2.8xlarge":  4029.600,
		"hi1.4xlarge": 2263.000,
		"hs1.8xlarge": 3358.000,
		"m3.medium":   48.910,
		"m3.large":    97.090,
		"m3.xlarge":   194.180,
		"m3.2xlarge":  388.360,
		"c3.large":    76.650,
		"c3.xlarge":   153.300,
		"c3.2xlarge":  306.600,
		"c3.4xlarge":  613.200,
		"c3.8xlarge":  1226.400,
		"m1.small":    32.120,
		"m1.medium":   63.510,
		"m1.large":    127.750,
		"m1.xlarge":   255.500,
		"c1.medium":   94.900,
		"c1.xlarge":   379.600,
		"m2.xlarge":   178.850,
		"m2.2xlarge":  357.700,
		"m2.4xlarge":  715.400,
		"t1.micro":    14.600,
		"cr1.8xlarge": 2555.000,
	}

	_, ok := price[InstanceType] //check the instance type, if not found - alert
	if !ok {
		fmt.Println("Price not found for ", InstanceType)
	}
	return price[InstanceType]
}

func main() {

	reportTable := map[string]float64{}
	constTable := map[string]string{}
	screds := credentials.NewSharedCredentials("/Users/ilyakravchenko/.aws/credentials", "myal")
	config := aws.Config{Region: aws.String("us-east-1"), Credentials: screds}
	sess := session.New(&config)
	if sess == nil {
		fmt.Println("problems with authorization")
	}
	svc := ec2.New(sess)
	params := &ec2.DescribeInstancesInput{}
	resp, err := svc.DescribeInstances(params)
	if err != nil {
		fmt.Println(err.Error())
		return
	}

	for index, _ := range resp.Reservations {
		for _, instance := range resp.Reservations[index].Instances {
			for _, tag := range instance.Tags {
				if *tag.Key == "Name" {
					extraInfo := *instance.InstanceType + "," + *instance.PrivateIpAddress //store extra info
					constTable[*tag.Value] = extraInfo
					_, ok := reportTable[*tag.Value]
					if !ok {
						reportTable[*tag.Value] = getPrice(*instance.InstanceType)

					} else {
						reportTable[*tag.Value] += getPrice(*instance.InstanceType)
					}
				}
			}
		}
	}
	for key, _ := range reportTable {
		_, ok := constTable[key]
		if ok {
			val := reportTable[key]
			constTable[key] = strconv.FormatFloat(val, 'f', 2, 64) + "," + constTable[key]
		}
	}
	table := tablewriter.NewWriter(os.Stdout)
	table.SetHeader([]string{"Type", "Price", "IP", "Name"})
	for k, v := range constTable {
		s := strings.Split(v, ",")
		s = []string{s[1], s[0], s[2]}

		table.Append(append(s, k))
	}
	table.Render()
}
