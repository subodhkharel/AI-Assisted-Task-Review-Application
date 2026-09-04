const STATUS_OPTIONS = [
  "NEW",
  "IN_PROGRESS",
  "COMPLETED",
];

/**
 * Render a single task card.
 *
 * @param {Object} props - Component properties.
 * @param {Object} props.task - Task data from the backend.
 * @param {Object|undefined} props.analysis - AI analysis result.
 * @param {boolean} props.isUpdating - Whether the task status is updating.
 * @param {boolean} props.isAnalysing - Whether AI analysis is running.
 * @param {Function} props.onStatusChange - Handle task status changes.
 * @param {Function} props.onAnalyse - Handle AI analysis.
 * @returns {JSX.Element} The task card UI.
 */
function TaskCard({
  task,
  analysis,
  isUpdating,
  isAnalysing,
  onStatusChange,
  onAnalyse,
}) {
  return (
    <li className="task-card">
      <h2>{task.title}</h2>

      <p>{task.description}</p>

      <div className="task-meta">
        <span>Priority: {task.priority}</span>

        <span>
          Created:{" "}
          {new Date(task.createdAt).toLocaleString()}
        </span>
      </div>

      <div className="status-control">
        <label htmlFor={`status-${task.id}`}>
          Status:
        </label>

        <select
          id={`status-${task.id}`}
          value={task.status}
          disabled={isUpdating}
          onChange={(event) => {
            onStatusChange(task.id, event.target.value);
          }}
        >
          {STATUS_OPTIONS.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>

        <button
          type="button"
          disabled={isAnalysing}
          onClick={() => {
            onAnalyse(task.id);
          }}
        >
          {isAnalysing
            ? "Analysing..."
            : "Analyse with AI"}
        </button>
      </div>

      {analysis && (
        <section className="analysis">
          <h3>AI Analysis</h3>

          <p>
            <strong>Category:</strong>{" "}
            {analysis.category}
          </p>

          <p>
            <strong>Priority:</strong>{" "}
            {analysis.priority}
          </p>

          <p>
            <strong>Summary:</strong>{" "}
            {analysis.summary}
          </p>

          <p>
            <strong>Recommended action:</strong>{" "}
            {analysis.recommendedAction}
          </p>
        </section>
      )}
    </li>
  );
}

export default TaskCard;
