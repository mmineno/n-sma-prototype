# app/models/user.rb
class User < ApplicationRecord
    has_many :notifications
    has_many :schedules
    has_many :documents
  end
  
  # app/models/notification.rb
  class Notification < ApplicationRecord
    belongs_to :user
  
    validates :title, presence: true
    validates :content, presence: true
    validates :date, presence: true
  end
  
  # app/models/schedule.rb
  class Schedule < ApplicationRecord
    belongs_to :user
  
    validates :title, presence: true
    validates :scheduled_at, presence: true
  end
  
  # app/models/document.rb
  class Document < ApplicationRecord
    belongs_to :user
  
    validates :document_type, presence: true
    validates :status, presence: true
    validates :updated_by, presence: true
    validates :updated_at, presence: true
  end
  
  # app/models/menu_item.rb
  class MenuItem < ApplicationRecord
    validates :name, presence: true
    validates :url, presence: true
  end
  