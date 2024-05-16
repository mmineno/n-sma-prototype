class Schedule < ApplicationRecord
    belongs_to :user
  
    validates :title, presence: true
    validates :scheduled_at, presence: true
  end