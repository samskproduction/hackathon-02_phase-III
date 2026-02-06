import { useState } from 'react';
import { Calendar, Flag, MoreHorizontal, Trash, Edit3, Circle, CheckCircle } from 'lucide-react';
import { Task } from '@/lib/types';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

export function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  const [showActions, setShowActions] = useState(false);

  // Priority badge styling
  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'urgent':
        return 'bg-red-500 text-white';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div
      className={`group flex items-start gap-4 rounded-lg border p-4 transition-all duration-200 ${
        task.isCompleted
          ? 'bg-muted/50 dark:bg-muted/20 opacity-75'
          : 'bg-background hover:bg-accent/50 dark:hover:bg-accent/20'
      }`}
      role="listitem"
      tabIndex={0}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="flex items-center gap-3">
        <button
          onClick={onToggle}
          className="flex items-center justify-center rounded-full transition-colors hover:bg-accent focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          aria-label={task.isCompleted ? "Mark as incomplete" : "Mark as complete"}
          aria-checked={task.isCompleted}
          role="checkbox"
        >
          {task.isCompleted ? (
            <CheckCircle className="h-5 w-5 text-primary" />
          ) : (
            <Circle className="h-5 w-5 text-muted-foreground" />
          )}
        </button>
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <h3
              className={`text-base font-medium truncate ${
                task.isCompleted
                  ? 'line-through text-muted-foreground'
                  : 'text-foreground'
              }`}
              id={`task-title-${task.id}`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p
                className={`mt-1 text-sm text-muted-foreground ${task.isCompleted ? 'line-through' : ''}`}
                id={`task-description-${task.id}`}
              >
                {task.description}
              </p>
            )}

            <div className="mt-2 flex flex-wrap items-center gap-2" aria-label="Task details">
              {task.priority && (
                <span
                  className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${getPriorityClass(task.priority)}`}
                  aria-label={`Priority: ${task.priority}`}
                >
                  <Flag className="mr-1 h-3 w-3" aria-hidden="true" />
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
              )}

              {task.dueDate && (
                <span
                  className="inline-flex items-center rounded-full bg-blue-100 px-2 py-1 text-xs font-medium text-blue-800 dark:bg-blue-900/30 dark:text-blue-300"
                  aria-label={`Due date: ${new Date(task.dueDate).toLocaleDateString()}`}
                >
                  <Calendar className="mr-1 h-3 w-3" aria-hidden="true" />
                  {new Date(task.dueDate).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>

          <div
            className={`flex items-center gap-1 transition-opacity ${
              showActions ? 'opacity-100' : 'opacity-0'
            }`}
            role="group"
            aria-label="Task actions"
          >
            <Button
              variant="ghost"
              size="icon"
              onClick={onEdit}
              className="h-8 w-8 focus:ring-2 focus:ring-primary focus:ring-offset-2"
              aria-label="Edit task"
              aria-describedby={`task-title-${task.id}`}
            >
              <Edit3 className="h-4 w-4" aria-hidden="true" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={onDelete}
              className="h-8 w-8 text-destructive hover:text-destructive focus:ring-2 focus:ring-destructive focus:ring-offset-2"
              aria-label="Delete task"
              aria-describedby={`task-title-${task.id}`}
            >
              <Trash className="h-4 w-4" aria-hidden="true" />
            </Button>
          </div>
        </div>

        <div className="mt-2 flex items-center justify-between">
          <div
            className="text-xs text-muted-foreground"
            aria-label={`Last updated: ${task.updatedAt ? new Date(task.updatedAt).toLocaleDateString() : ''}`}
          >
            {task.updatedAt ? `Updated ${new Date(task.updatedAt).toLocaleDateString()}` : ''}
          </div>
        </div>
      </div>
    </div>
  );
}