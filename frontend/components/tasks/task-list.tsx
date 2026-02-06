import { Task } from '@/lib/types';
import { TaskItem } from '@/components/tasks/task-item';

interface TaskListProps {
  tasks: Task[];
  onTaskToggle: (id: string) => void;
  onTaskEdit: (task: Task) => void;
  onTaskDelete: (id: string) => void;
}

export function TaskList({ tasks, onTaskToggle, onTaskEdit, onTaskDelete }: TaskListProps) {
  // Separate completed and active tasks
  const completedTasks = tasks.filter(task => task.isCompleted);
  const activeTasks = tasks.filter(task => !task.isCompleted);

  return (
    <div className="space-y-4">
      {activeTasks.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-3 text-muted-foreground">Active Tasks</h2>
          <div className="space-y-3">
            {activeTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={() => onTaskToggle(task.id)}
                onEdit={() => onTaskEdit(task)}
                onDelete={() => onTaskDelete(task.id)}
              />
            ))}
          </div>
        </div>
      )}

      {completedTasks.length > 0 && (
        <div className="pt-6 border-t">
          <h2 className="text-lg font-semibold mb-3 text-muted-foreground">Completed</h2>
          <div className="space-y-3">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={() => onTaskToggle(task.id)}
                onEdit={() => onTaskEdit(task)}
                onDelete={() => onTaskDelete(task.id)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}