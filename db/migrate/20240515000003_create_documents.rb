class CreateDocuments < ActiveRecord::Migration[6.1]
    def change
      create_table :documents do |t|
        t.references :user, null: false, foreign_key: true
        t.string :document_type, null: false
        t.string :status, null: false
        t.string :updated_by, null: false
        t.datetime :updated_at, null: false
  
        t.timestamps
      end
    end
  end