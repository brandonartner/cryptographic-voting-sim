class AddVoterIdRefToDocuments < ActiveRecord::Migration[5.1]
  def change
	add_reference :documents, :voter_id, foreign_key: true
  end
end
