class DashboardController < ApplicationController
    def index
      @user = current_user
      @notifications = @user.notifications.order(date: :desc).limit(5)
      @today_schedules = @user.schedules.where('scheduled_at >= ? AND scheduled_at < ?', Date.today.beginning_of_day, Date.today.end_of_day)
      @pending_documents = @user.documents.where(status: 'pending')
      @menu_items = MenuItem.all
    end
  end