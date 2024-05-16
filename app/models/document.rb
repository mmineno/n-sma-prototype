class Document < ApplicationRecord
    belongs_to :user
  
    validates :document_type, presence: true
    validates :status, presence: true
    validates :updated_by, presence: true
    validates :updated_at, presence: true
  end