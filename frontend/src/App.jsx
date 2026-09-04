import { useEffect, useState } from "react";
import TaskCard from "./components/TaskCard";


import {
  analyseTask,
  fetchTasks,
  updateTaskStatus,
} from "./api";

import "./App.css";

const STATUS_OPTIONS = [
  "NEW",
  "IN_PROGRESS",
  "COMPLETED",
];

/**
 * Render the task review application.
 *
 * @returns {JSX.Element} The task review UI.
 */
function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [updatingTaskId, setUpdatingTaskId] = useState(null);
  const [analysis, setAnalysis] = useState({});
  const [analysingTaskId, setAnalysingTaskId] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    loadTasks(selectedStatus);
  }, [selectedStatus]);

  /**
   * Load tasks using the currently selected status filter.
   *
   * @param {string} status - The selected status filter.
   * @returns {Promise<void>}
   */
  async function loadTasks(status) {
    try {
      setIsLoading(true);
      setError("");

      const data = await fetchTasks(status);

      setTasks(data);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  /**
   * Update a task's status and refresh the task list.
   *
   * @param {number} taskId - The task ID.
   * @param {string} status - The new status.
   * @returns {Promise<void>}
   */
  async function handleStatusChange(taskId, status) {
    try {
      setUpdatingTaskId(taskId);
      setError("");

      await updateTaskStatus(taskId, status);
      await loadTasks(selectedStatus);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setUpdatingTaskId(null);
    }
  }

  /**
   * Analyse a task and store its AI result.
   *
   * @param {number} taskId - The task ID.
   * @returns {Promise<void>}
   */
  async function handleAnalyse(taskId) {
    try {
      setAnalysingTaskId(taskId);
      setError("");

      const result = await analyseTask(taskId);

      setAnalysis((currentAnalysis) => ({
        ...currentAnalysis,
        [taskId]: result,
      }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setAnalysingTaskId(null);
    }
  }

  return (
    <main>
      <h1>Task Review</h1>

      <div className="filter">
        <label htmlFor="status-filter">
          Filter by status:
        </label>

        <select
          id="status-filter"
          value={selectedStatus}
          onChange={(event) => {
            setSelectedStatus(event.target.value);
          }}
        >
          <option value="">All</option>

          {STATUS_OPTIONS.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>

      {error && <p className="error">{error}</p>}

      {isLoading ? (
        <p>Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <ul className="task-list">

          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              analysis={analysis[task.id]}
              isUpdating={updatingTaskId === task.id}
              isAnalysing={analysingTaskId === task.id}
              onStatusChange={handleStatusChange}
              onAnalyse={handleAnalyse}
            />
          ))}
        </ul>
      )}
    </main>
  );
}

export default App;
