class CreateNotifications < ActiveRecord::Migration[6.1]
    def change
      create_table :notifications do |t|
        t.references :user, null: false, foreign_key: true
        t.string :title, null: false
        t.text :content, null: false
        t.date :date, null: false
  
        t.timestamps
      end
    end
  end