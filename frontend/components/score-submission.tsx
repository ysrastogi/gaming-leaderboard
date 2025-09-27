"use client"

import type React from "react"

import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertCircle, CheckCircle, Loader2 } from "lucide-react"
import { useState } from "react"

interface SubmissionState {
  loading: boolean
  success: boolean
  error: string | null
}

const API_URL = "http://localhost:8000"

export default function ScoreSubmission() {
  const [userId, setUserId] = useState("")
  const [score, setScore] = useState("")
  const [state, setState] = useState<SubmissionState>({
    loading: false,
    success: false,
    error: null,
  })

  const validateForm = () => {
    if (!userId.trim()) {
      setState((prev) => ({ ...prev, error: "User ID is required" }))
      return false
    }
    if (!score.trim()) {
      setState((prev) => ({ ...prev, error: "Score is required" }))
      return false
    }
    const scoreNum = Number.parseInt(score)
    if (isNaN(scoreNum) || scoreNum < 0) {
      setState((prev) => ({ ...prev, error: "Score must be a valid positive number" }))
      return false
    }
    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) return

    setState({ loading: true, success: false, error: null })

    try {
      const response = await fetch(`${API_URL}/api/leaderboard/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId.trim(), // Convert to number as expected by API
          score: parseInt(score.trim()),
          game_mode: "SOLO", // Default to SOLO mode, can be expanded with a dropdown
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Failed to submit score")
      }

      const data = await response.json()
      setState({ loading: false, success: true, error: null })

      // Optional: Reset form after successful submission
      setUserId("")
      setScore("")
    } catch (error) {
      setState({
        loading: false,
        success: false,
        error: error instanceof Error ? error.message : "Failed to submit score",
      })
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="userId">User ID</Label>
            <Input
              id="userId"
              type="text"
              placeholder="Enter your user ID"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              disabled={state.loading}
              className="w-full"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="score">Score</Label>
            <Input
              id="score"
              type="number"
              placeholder="Enter your score"
              value={score}
              onChange={(e) => setScore(e.target.value)}
              disabled={state.loading}
              min="0"
              className="w-full"
            />
          </div>
        </div>

        <Button type="submit" disabled={state.loading} className="w-full md:w-auto">
          {state.loading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Submitting...
            </>
          ) : (
            "Submit Score"
          )}
        </Button>
      </form>

      {/* Status Messages */}
      {state.success && (
        <Alert className="border-green-200 bg-green-50 text-green-800">
          <CheckCircle className="h-4 w-4" />
          <AlertDescription>
            Score submitted successfully! Your score has been added to the leaderboard.
          </AlertDescription>
        </Alert>
      )}

      {state.error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{state.error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}
