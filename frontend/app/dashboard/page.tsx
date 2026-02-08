'use client';

import { useState, useEffect } from 'react';
import { Plus, Calendar, Flag, Circle, CheckCircle, LogOut } from 'lucide-react';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/lib/types';
import { TaskList } from '@/components/tasks/task-list';
import { TaskForm } from '@/components/tasks/task-form';
import { Button } from '@/components/ui/button';
import { Modal } from '@/components/ui/modal';
import { useAuth } from '@/providers/better-auth-provider';
import { apiClient } from '@/lib/api';
import ChatbotIcon from '@/components/ChatbotIcon';
import ChatWindow from '@/components/ChatWindow';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const { logout, user, isAuthenticated } = useAuth();

  useEffect(() => {
    // Fetch tasks from API
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      // Fetch tasks from API
      const response = await apiClient.getTasks();
      if (response.success) {
        // Map backend task format to frontend Task type
        const mappedTasks = response.data?.tasks?.map((backendTask: any) => ({
          id: String(backendTask.id),
          userId: backendTask.user_id,
          title: backendTask.title,
          description: backendTask.description,
          isCompleted: Boolean(backendTask.is_completed),
          createdAt: new Date(backendTask.created_at),
          updatedAt: new Date(backendTask.updated_at),
          dueDate: backendTask.due_date ? new Date(backendTask.due_date) : undefined,
          priority: backendTask.priority,
        })) || [];
        setTasks(mappedTasks);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const openChat = () => {
    setIsChatOpen(true);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  const handleTaskSubmit = async (taskData: CreateTaskRequest | UpdateTaskRequest) => {
    try {
      if (editingTask) {
        // Update existing task
        const response = await apiClient.updateTask(editingTask.id, taskData as UpdateTaskRequest);
        if (response.success && response.data) {
          const updatedTasks = tasks.map(t =>
            t.id === editingTask.id ? response.data!.task : t
          );
          setTasks(updatedTasks);
        }
      } else {
        // Create new task
        const response = await apiClient.createTask(taskData as CreateTaskRequest);
        if (response.success && response.data) {
          setTasks([response.data.task, ...tasks]);
        }
      }

      setShowTaskModal(false);
      setEditingTask(null);
    } catch (error) {
      console.error('Error saving task:', error);
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      const response = await apiClient.deleteTask(taskId);
      if (response.success) {
        setTasks(tasks.filter(task => task.id !== taskId));
      }
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleTaskToggle = async (taskId: string) => {
    try {
      const response = await apiClient.toggleTaskCompletion(taskId);
      if (response.success && response.data) {
        setTasks(tasks.map(task =>
          task.id === taskId ? response.data!.task : task
        ));
      }
    } catch (error) {
      console.error('Error toggling task:', error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskModal(true);
  };

  const handleLogout = async () => {
    try {
      await logout();
      // Redirect to login page after logout
      window.location.href = '/auth/login';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="container mx-auto py-10">
      <div className="mb-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">My Tasks</h1>
            <p className="text-muted-foreground">
              Manage your tasks efficiently and stay productive
            </p>
          </div>
          <Button variant="outline" onClick={handleLogout} className="flex items-center">
            <LogOut className="mr-2 h-4 w-4" />
            Sign Out
          </Button>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <div className="flex items-center space-x-4 mb-4 sm:mb-0">
          <Button onClick={() => setShowTaskModal(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add Task
          </Button>
        </div>

        <div className="flex items-center space-x-2 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4" />
          <span>Today: {new Date().toLocaleDateString()}</span>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="p-4 border rounded-lg animate-pulse">
              <div className="flex items-center space-x-3">
                <div className="h-5 w-5 rounded bg-muted"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-muted rounded w-3/4"></div>
                  <div className="h-3 bg-muted rounded w-1/2"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : tasks.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 border-2 border-dashed rounded-lg">
          <div className="text-center max-w-md">
            <Flag className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No tasks yet</h3>
            <p className="text-muted-foreground mb-4">
              Get started by creating your first task to stay organized and productive.
            </p>
            <Button onClick={() => setShowTaskModal(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Create your first task
            </Button>
          </div>
        </div>
      ) : (
        <TaskList
          tasks={tasks}
          onTaskToggle={handleTaskToggle}
          onTaskEdit={handleEditTask}
          onTaskDelete={handleTaskDelete}
        />
      )}

      <Modal
        isOpen={showTaskModal}
        onClose={() => {
          setShowTaskModal(false);
          setEditingTask(null);
        }}
        title={editingTask ? "Edit Task" : "Create New Task"}
      >
        <TaskForm
          task={editingTask}
          onSubmit={handleTaskSubmit}
          onCancel={() => {
            setShowTaskModal(false);
            setEditingTask(null);
          }}
        />
      </Modal>

      {/* Chatbot components */}
      <ChatbotIcon onOpen={openChat} />
      <ChatWindow isOpen={isChatOpen} onClose={closeChat} />
    </div>
  );
}