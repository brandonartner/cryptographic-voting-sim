class CreateDocuments < ActiveRecord::Migration[5.1]
  def change
    create_table :documents do |t|
      t.string :title
      t.text :text
      t.integer :voter_id

      t.timestamps
    end
  end
end
