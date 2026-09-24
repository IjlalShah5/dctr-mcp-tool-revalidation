package main

import (
	"os"
	"reflect"
	"testing"
)

func TestDefaultIsSafe(t *testing.T) {
	os.Unsetenv("ENABLE_TF_OPERATIONS")
	got := selectedCreateRunContract()
	if got.Variant != "CreateRunSafe" || got.DestructiveHint {
		t.Fatalf("default did not select safe contract: %+v", got)
	}
	want := []string{"plan_and_apply", "refresh_state", "plan_only", "allow_empty_apply"}
	if !reflect.DeepEqual(got.RunTypeEnum, want) {
		t.Fatalf("safe enum mismatch: got=%v want=%v", got.RunTypeEnum, want)
	}
}

func TestFalseIsSafe(t *testing.T) {
	os.Setenv("ENABLE_TF_OPERATIONS", "false")
	got := selectedCreateRunContract()
	if got.Variant != "CreateRunSafe" || got.DestructiveHint {
		t.Fatalf("false did not select safe contract: %+v", got)
	}
}

func TestTrueIsDestructiveVariant(t *testing.T) {
	os.Setenv("ENABLE_TF_OPERATIONS", "TrUe")
	got := selectedCreateRunContract()
	if got.Variant != "CreateRun" || !got.DestructiveHint {
		t.Fatalf("true did not select destructive contract: %+v", got)
	}
	want := []string{
		"plan_and_apply", "refresh_state", "plan_only",
		"allow_empty_apply", "auto_approve", "is_destroy",
	}
	if !reflect.DeepEqual(got.RunTypeEnum, want) {
		t.Fatalf("destructive enum mismatch: got=%v want=%v", got.RunTypeEnum, want)
	}
}
