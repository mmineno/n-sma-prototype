class User < ApplicationRecord
    has_many :notifications
    has_many :schedules
    has_many :documents
  end