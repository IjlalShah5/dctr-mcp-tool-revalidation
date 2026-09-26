package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type Contract struct {
	Variant         string   `json:"variant"`
	DestructiveHint bool     `json:"destructiveHint"`
	RunTypeEnum     []string `json:"runTypeEnum"`
}

func isTerraformOperationsEnabled() bool {
	envVar := os.Getenv("ENABLE_TF_OPERATIONS")
	if envVar == "" {
		envVar = "false"
	}
	return strings.ToLower(envVar) == "true"
}

func selectedCreateRunContract() Contract {
	if isTerraformOperationsEnabled() {
		return Contract{
			Variant: "CreateRun",
			DestructiveHint: true,
			RunTypeEnum: []string{
				"plan_and_apply", "refresh_state", "plan_only",
				"allow_empty_apply", "auto_approve", "is_destroy",
			},
		}
	}
	return Contract{
		Variant: "CreateRunSafe",
		DestructiveHint: false,
		RunTypeEnum: []string{
			"plan_and_apply", "refresh_state", "plan_only", "allow_empty_apply",
		},
	}
}

func main() {
	out, _ := json.MarshalIndent(selectedCreateRunContract(), "", "  ")
	fmt.Println(string(out))
}
