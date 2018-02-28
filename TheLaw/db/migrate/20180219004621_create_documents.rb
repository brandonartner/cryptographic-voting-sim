class CreateDocuments < ActiveRecord::Migration[5.1]
  def change
    create_table :documents do |t|
      t.string :name
      t.text :body
      t.integer :voter_id

      t.timestamps
    end
  end
end
