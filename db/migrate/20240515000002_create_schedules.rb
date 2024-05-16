class CreateSchedules < ActiveRecord::Migration[6.1]
    def change
      create_table :schedules do |t|
        t.references :user, null: false, foreign_key: true
        t.string :title, null: false
        t.datetime :scheduled_at, null: false
  
        t.timestamps
      end
    end
  end