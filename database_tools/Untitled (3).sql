CREATE TABLE [user] (
  [id] uuid PRIMARY KEY,
  [email] email,
  [full_name] varchar(255),
  [username] email,
  [phone_number] varchar(255),
  [identification_number_card] varchar(255),
  [user_type] varchar(255),
  [is_active] boolean,
  [is_staff] boolean,
  [is_admin] boolean,
  [created_on] datetime DEFAULT (now())
)
GO

CREATE TABLE [province] (
  [id] uuid PRIMARY KEY,
  [name] varchar(255)
)
GO

CREATE TABLE [district] (
  [id] uuid PRIMARY KEY,
  [name] varchar(255),
  [province] uuid
)
GO

CREATE TABLE [sector] (
  [id] uuid PRIMARY KEY,
  [name] varchar(255),
  [district] uuid
)
GO

CREATE TABLE [village] (
  [id] uuid PRIMARY KEY,
  [name] varchar(255),
  [sector] uuid
)
GO

CREATE TABLE [userAddress] (
  [id] uuid PRIMARY KEY,
  [user] uuid,
  [village] uuid
)
GO

CREATE TABLE [patient] (
  [id] uuid PRIMARY KEY,
  [full_name] varchar(255),
  [insurance_name] varchar(255),
  [insurance_number] varchar(255),
  [sickness] varchar(255),
  [phone] varchar(255),
  [village] uuid,
  [date_of_birth] date,
  [worker] uuid,
  [created_on] datetime DEFAULT (now())
)
GO

CREATE TABLE [houseHold] (
  [id] uuid PRIMARY KEY,
  [father_full_name] varchar(255),
  [father_id_no] varchar(255),
  [mother_full_name] varchar(255),
  [mother_id_no] varchar(255),
  [number_child] int DEFAULT (0),
  [phone_number] varchar(255),
  [worker] uuid,
  [village] uuid,
  [created_on] datetime DEFAULT (now())
)
GO

CREATE TABLE [Malnutrition] (
  [id] uuid PRIMARY KEY,
  [family] uuid,
  [child_full_name] varchar(255),
  [has_malnutrition] boolean DEFAULT (true),
  [worker] uuid,
  [created_on] datetime DEFAULT (now())
)
GO

CREATE TABLE [contraceprion] (
  [id] uuid PRIMARY KEY,
  [family] uuid,
  [description] text,
  [worker] uuid,
  [created_on] datetime DEFAULT (now())
)
GO

ALTER TABLE [district] ADD FOREIGN KEY ([province]) REFERENCES [province] ([id])
GO

ALTER TABLE [sector] ADD FOREIGN KEY ([district]) REFERENCES [district] ([id])
GO

ALTER TABLE [village] ADD FOREIGN KEY ([sector]) REFERENCES [sector] ([id])
GO

ALTER TABLE [userAddress] ADD FOREIGN KEY ([user]) REFERENCES [user] ([id])
GO

ALTER TABLE [userAddress] ADD FOREIGN KEY ([village]) REFERENCES [village] ([id])
GO

ALTER TABLE [patient] ADD FOREIGN KEY ([village]) REFERENCES [village] ([id])
GO

ALTER TABLE [patient] ADD FOREIGN KEY ([worker]) REFERENCES [user] ([id])
GO

ALTER TABLE [houseHold] ADD FOREIGN KEY ([worker]) REFERENCES [user] ([id])
GO

ALTER TABLE [houseHold] ADD FOREIGN KEY ([village]) REFERENCES [village] ([id])
GO

ALTER TABLE [Malnutrition] ADD FOREIGN KEY ([family]) REFERENCES [houseHold] ([id])
GO

ALTER TABLE [Malnutrition] ADD FOREIGN KEY ([worker]) REFERENCES [user] ([id])
GO

ALTER TABLE [contraceprion] ADD FOREIGN KEY ([family]) REFERENCES [houseHold] ([id])
GO

ALTER TABLE [contraceprion] ADD FOREIGN KEY ([worker]) REFERENCES [user] ([id])
GO
