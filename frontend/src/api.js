const API_BASE_URL = "http://127.0.0.1:8000/api";

/**
 * Fetch tasks from the backend.
 *
 * @param {string} status - Optional task status filter.
 * @returns {Promise<Array>} The list of tasks.
 * @throws {Error} If the API request fails.
 */
export async function fetchTasks(status = "") {
  const query = status
    ? `?status=${encodeURIComponent(status)}`
    : "";

  const response = await fetch(
    `${API_BASE_URL}/tasks/${query}`,
  );

  if (!response.ok) {
    throw new Error("Failed to load tasks.");
  }

  return response.json();
}

/**
 * Update the status of a task.
 *
 * @param {number} taskId - The task ID.
 * @param {string} status - The new task status.
 * @returns {Promise<Object>} The updated task status response.
 * @throws {Error} If the API request fails.
 */
export async function updateTaskStatus(taskId, status) {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}/status/`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status }),
    },
  );

  if (!response.ok) {
    throw new Error("Failed to update task status.");
  }

  return response.json();
}


/**
 * Analyse a task using the backend AI service.
 *
 * @param {number} taskId - The task ID.
 * @returns {Promise<Object>} The structured task analysis.
 * @throws {Error} If the analysis request fails.
 */
export async function analyseTask(taskId) {
  const response = await fetch(
    `${API_BASE_URL}/tasks/${taskId}/analyse/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

  if (!response.ok) {
    const data = await response.json().catch(() => null);

    throw new Error(
      data?.detail || "Failed to analyse task.",
    );
  }

  return response.json();
}
