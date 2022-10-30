from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    ALTER TABLE `adminrole` DROP FOREIGN KEY `adminrole_ibfk_1`;
    ALTER TABLE `attachments` DROP FOREIGN KEY `attachments_ibfk_1`;
    ALTER TABLE `bugreportingchannel` DROP FOREIGN KEY `bugreportingchannel_ibfk_1`;
    ALTER TABLE `bugreportingchannel` DROP FOREIGN KEY `bugreportingchannel_ibfk_2`;
    ALTER TABLE `krillbylines` DROP FOREIGN KEY `krillbylines_ibfk_1`;
    ALTER TABLE `krillconfig` DROP FOREIGN KEY `krillconfig_ibfk_1`;
    ALTER TABLE `localization` DROP FOREIGN KEY `localization_ibfk_1`;
    ALTER TABLE `modrole` DROP FOREIGN KEY `modrole_ibfk_1`;
    ALTER TABLE `repros` DROP FOREIGN KEY `repros_ibfk_1`;
    ALTER TABLE `trustedrole` DROP FOREIGN KEY `trustedrole_ibfk_1`;
    ALTER TABLE `userpermission` DROP FOREIGN KEY `userpermission_ibfk_1`;
    ALTER TABLE `watchedemoji` DROP FOREIGN KEY `watchedemoji_ibfk_1`;
        """ + """
    ALTER TABLE `bugreport` DROP KEY `bugreport_attachment_message_id`;
    ALTER TABLE `bugreport` DROP KEY `bugreport_message_id`;
    ALTER TABLE `bugreportingchannel` DROP KEY `bugreportingchannel_channelid`;
    ALTER TABLE `bugreportingchannel` DROP KEY `bugreportingchannel_guild_id_platform_id`;
    ALTER TABLE `bugreportingplatform` DROP KEY `bugreportingplatform_platform_branch`;
    ALTER TABLE `krillconfig` DROP KEY `krillconfig_guild_id`;
        """ + """
    DROP INDEX `adminrole_guild_id` ON `adminrole`;
    DROP INDEX `attachements_report_id` ON `attachments`;
    DROP INDEX `bugreportingchannel_guild_id` ON `bugreportingchannel`;
    DROP INDEX `bugreportingchannel_platform_id` ON `bugreportingchannel`;
    DROP INDEX `krillbylines_krill_config_id` ON `krillbylines`;
    DROP INDEX `localization_guild_id` ON `localization`;
    DROP INDEX `modrole_guild_id` ON `modrole`;
    DROP INDEX `repros_report_id` ON `repros`;
    DROP INDEX `trustedrole_guild_id` ON `trustedrole`;
    DROP INDEX `userpermission_guild_id` ON `userpermission`;
    DROP INDEX `watchedemoji_watcher_id` ON `watchedemoji`;
        """ + """
    ALTER DATABASE sky CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    ALTER TABLE `adminrole` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `artchannel` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `botadmin` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `bugreportingchannel` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `bugreportingplatform` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `configchannel` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `countword` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `dropboxchannel` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `guild` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `krillbylines` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `krillchannel` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `krillconfig` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `localization` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `modrole` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `oreoletters` COLLATE = utf8mb4_bin;
    ALTER TABLE `oreoletters` MODIFY token VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
    ALTER TABLE `oreomap` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `reactwatch` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `trustedrole` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `userpermission` COLLATE = utf8mb4_general_ci;
    ALTER TABLE `watchedemoji` COLLATE = utf8mb4_bin;
        """ + """
    ALTER TABLE `artchannel` ALTER COLUMN `listenchannelid` SET DEFAULT 0;
    ALTER TABLE `artchannel` ALTER COLUMN `collectionchannelid` SET DEFAULT 0;
    ALTER TABLE `autoresponder` ALTER COLUMN `chance` SET DEFAULT 10000;
    ALTER TABLE `autoresponder` ALTER COLUMN `responsechannelid` SET DEFAULT 0;
    ALTER TABLE `autoresponder` ALTER COLUMN `listenchannelid` SET DEFAULT 0;
    ALTER TABLE `autoresponder` ALTER COLUMN `logchannelid` SET DEFAULT 0;
    ALTER TABLE `configchannel` ALTER COLUMN `channelid` SET DEFAULT 0;
    ALTER TABLE `customcommand` ALTER COLUMN `deletetrigger` SET DEFAULT 0;
    ALTER TABLE `customcommand` ALTER COLUMN `reply` SET DEFAULT 0;
    ALTER TABLE `dropboxchannel` ALTER COLUMN `targetchannelid` SET DEFAULT 0;
    ALTER TABLE `dropboxchannel` ALTER COLUMN `deletedelayms` SET DEFAULT 0;
    ALTER TABLE `dropboxchannel` ALTER COLUMN `sendreceipt` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `memberrole` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `nonmemberrole` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `mutedrole` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `betarole` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `welcomechannelid` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `ruleschannelid` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `logchannelid` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `entrychannelid` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `maintenancechannelid` SET DEFAULT 0;
    ALTER TABLE `guild` ALTER COLUMN `rulesreactmessageid` SET DEFAULT 0;
    ALTER TABLE `krillbylines` ALTER COLUMN `type` SET DEFAULT 0;
    ALTER TABLE `krillbylines` ALTER COLUMN `channelid` SET DEFAULT 0;
    ALTER TABLE `krillbylines` ALTER COLUMN `locale` SET DEFAULT '';
    ALTER TABLE `krillconfig` ALTER COLUMN `return_home_freq` SET DEFAULT 0;
    ALTER TABLE `krillconfig` ALTER COLUMN `shadow_roll_freq` SET DEFAULT 0;
    ALTER TABLE `krillconfig` ALTER COLUMN `krill_rider_freq` SET DEFAULT 0;
    ALTER TABLE `krillconfig` ALTER COLUMN `crab_freq` SET DEFAULT 0;
    ALTER TABLE `krillconfig` ALTER COLUMN `allow_text` SET DEFAULT 1;
    ALTER TABLE `krillconfig` ALTER COLUMN `monster_duration` SET DEFAULT 21600;
    ALTER TABLE `localization` ALTER COLUMN `channelid` SET DEFAULT 0;
    ALTER TABLE `localization` ALTER COLUMN `locale` SET DEFAULT '';
    ALTER TABLE `oreomap` ALTER COLUMN `letter_o` SET DEFAULT 1;
    ALTER TABLE `oreomap` ALTER COLUMN `letter_r` SET DEFAULT 2;
    ALTER TABLE `oreomap` ALTER COLUMN `letter_e` SET DEFAULT 3;
    ALTER TABLE `oreomap` ALTER COLUMN `letter_oh` SET DEFAULT 4;
    ALTER TABLE `oreomap` ALTER COLUMN `letter_re` SET DEFAULT 5;
    ALTER TABLE `oreomap` ALTER COLUMN `space_char` SET DEFAULT 6;
    ALTER TABLE `reactwatch` ALTER COLUMN `muteduration` SET DEFAULT 600;
    ALTER TABLE `reactwatch` ALTER COLUMN `watchremoves` SET DEFAULT 0;
    ALTER TABLE `userpermission` ALTER COLUMN `command` SET DEFAULT '';
    ALTER TABLE `userpermission` ALTER COLUMN `allow` SET DEFAULT 1;
    ALTER TABLE `watchedemoji` ALTER COLUMN `log` SET DEFAULT 0;
    ALTER TABLE `watchedemoji` ALTER COLUMN `remove` SET DEFAULT 0;
    ALTER TABLE `watchedemoji` ALTER COLUMN `mute` SET DEFAULT 0;
        """ + """
    ALTER TABLE `artchannel` MODIFY `tag` VARCHAR(30) DEFAULT '' NOT NULL;
    ALTER TABLE `autoresponder` MODIFY `flags` SMALLINT DEFAULT 0 NOT NULL;
    ALTER TABLE `bugreportingplatform` MODIFY `platform` VARCHAR(100) NOT NULL;
    ALTER TABLE `bugreportingplatform` MODIFY `branch` VARCHAR(20) NOT NULL;
    ALTER TABLE `configchannel` MODIFY `configname` VARCHAR(100) NOT NULL;
    ALTER TABLE `countword` MODIFY `word` VARCHAR(300) NOT NULL;
    ALTER TABLE `krillbylines` MODIFY `byline` VARCHAR(100) NOT NULL;
    ALTER TABLE `oreoletters` MODIFY `token` VARCHAR(50) DEFAULT '' NOT NULL;
    ALTER TABLE `oreomap` MODIFY `char_count` VARCHAR(50) DEFAULT '{0,10}' NOT NULL;
    ALTER TABLE `watchedemoji` MODIFY `emoji` VARCHAR(50) NOT NULL;
        """ + """
    ALTER TABLE `adminrole` ADD CONSTRAINT `uid_adminrole_roleid_457f6b` UNIQUE (`roleid`, `guild_id`);
    ALTER TABLE `artchannel` ADD CONSTRAINT `uid_artchannel_serveri_dacf81` UNIQUE (`serverid`, `listenchannelid`, `collectionchannelid`, `tag`);
    # ALTER TABLE `attachments` ADD CONSTRAINT `uid_attachments_report__89548d` UNIQUE (`report_id`, `url`(100));
    ALTER TABLE `autoresponder` ADD CONSTRAINT `uid_autorespond_trigger_d7d834` UNIQUE (`trigger`, `serverid`);
    ALTER TABLE `botadmin` ADD CONSTRAINT `userid` UNIQUE (`userid`);
    ALTER TABLE `bugreport` ADD CONSTRAINT `attachment_message_id` UNIQUE (`attachment_message_id`);
    ALTER TABLE `bugreport` ADD CONSTRAINT `message_id` UNIQUE (`message_id`);
    ALTER TABLE `bugreportingchannel` ADD CONSTRAINT `uid_bugreportin_guild_i_91e902` UNIQUE (`guild_id`, `platform_id`);
    ALTER TABLE `bugreportingplatform` ADD CONSTRAINT `uid_bugreportin_platfor_fb781e` UNIQUE (`platform`, `branch`);
    ALTER TABLE `configchannel` ADD CONSTRAINT `uid_configchann_confign_21c1ab` UNIQUE (`configname`, `serverid`);
    ALTER TABLE `countword` ADD CONSTRAINT `uid_countword_word_931444` UNIQUE (`word`, `serverid`);
    ALTER TABLE `customcommand` ADD CONSTRAINT `uid_customcomma_trigger_65c25c` UNIQUE (`trigger`, `serverid`);
    ALTER TABLE `dropboxchannel` ADD CONSTRAINT `uid_dropboxchan_serveri_7254d9` UNIQUE (`serverid`, `sourcechannelid`);
    ALTER TABLE `guild` ADD CONSTRAINT `serverid` UNIQUE (`serverid`);
    ALTER TABLE `krillbylines` ADD CONSTRAINT `uid_krillbyline_krill_c_b18cc4` UNIQUE (`krill_config_id`, `byline`, `type`);
    ALTER TABLE `krillchannel` ADD CONSTRAINT `uid_krillchanne_serveri_5da66e` UNIQUE (`serverid`, `channelid`);
    ALTER TABLE `krillconfig` ADD CONSTRAINT `guild_id` UNIQUE (`guild_id`);
    ALTER TABLE `localization` ADD CONSTRAINT `uid_localizatio_guild_i_1e041d` UNIQUE (`guild_id`, `channelid`);
    ALTER TABLE `modrole` ADD CONSTRAINT `uid_modrole_roleid_b1b1c0` UNIQUE (`roleid`, `guild_id`);
    ALTER TABLE `oreoletters` ADD CONSTRAINT `uid_oreoletters_token_84fe18` UNIQUE (`token`, `token_class`);
    ALTER TABLE `reactwatch` ADD CONSTRAINT `serverid` UNIQUE (`serverid`);
    ALTER TABLE `repros` ADD CONSTRAINT `uid_repros_user_34d996` UNIQUE (`user`, `report_id`);
    ALTER TABLE `trustedrole` ADD CONSTRAINT `uid_trustedrole_roleid_215f34` UNIQUE (`roleid`, `guild_id`);
    ALTER TABLE `userpermission` ADD CONSTRAINT `uid_userpermiss_userid_7b40ae` UNIQUE (`userid`, `command`);
    ALTER TABLE `watchedemoji` ADD CONSTRAINT `uid_watchedemoj_emoji_4203dc` UNIQUE (`emoji`, `watcher_id`);
        """ + """
    ALTER TABLE `adminrole` ADD CONSTRAINT `fk_adminrol_guild_56368cba` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `attachments` ADD CONSTRAINT `fk_attachme_bugrepor_0d8fd583` FOREIGN KEY (`report_id`) REFERENCES `bugreport` (`id`) ON DELETE CASCADE;
    ALTER TABLE `bugreportingchannel` ADD CONSTRAINT `fk_bugrepor_bugrepor_2f3979ee` FOREIGN KEY (`platform_id`) REFERENCES `bugreportingplatform` (`id`) ON DELETE CASCADE;
    ALTER TABLE `bugreportingchannel` ADD CONSTRAINT `fk_bugrepor_guild_04eb4078` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `krillbylines` ADD CONSTRAINT `fk_krillbyl_krillcon_04799d75` FOREIGN KEY (`krill_config_id`) REFERENCES `krillconfig` (`id`) ON DELETE CASCADE;
    ALTER TABLE `krillconfig` ADD CONSTRAINT `fk_krillcon_guild_43a114df` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `localization` ADD CONSTRAINT `fk_localiza_guild_9f755aae` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `modrole` ADD CONSTRAINT `fk_modrole_guild_62488d68` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `repros` ADD CONSTRAINT `fk_repros_bugrepor_b26170f5` FOREIGN KEY (`report_id`) REFERENCES `bugreport` (`id`) ON DELETE CASCADE;
    ALTER TABLE `trustedrole` ADD CONSTRAINT `fk_trustedr_guild_7af9759e` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `userpermission` ADD CONSTRAINT `fk_userperm_guild_24ce9edd` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`) ON DELETE CASCADE;
    ALTER TABLE `watchedemoji` ADD CONSTRAINT `fk_watchede_reactwat_b8aaa411` FOREIGN KEY (`watcher_id`) REFERENCES `reactwatch` (`id`) ON DELETE CASCADE;
        """ + """
    CREATE INDEX `idx_adminrole_guild_i_1576b8` ON `adminrole` (`guild_id`);
    CREATE INDEX `idx_attachments_report__4bd92e` ON `attachments` (`report_id`);
    CREATE INDEX `idx_bugreportin_guild_i_e13b1e` ON `bugreportingchannel` (`guild_id`);
    CREATE INDEX `idx_bugreportin_platfor_fe0d79` ON `bugreportingchannel` (`platform_id`);
    CREATE INDEX `idx_krillbyline_krill_c_95a61d` ON `krillbylines` (`krill_config_id`);
    CREATE INDEX `idx_krillconfig_guild_i_bc8ec8` ON `krillconfig` (`guild_id`);
    CREATE INDEX `idx_localizatio_guild_i_2a3780` ON `localization` (`guild_id`);
    CREATE INDEX `idx_modrole_guild_i_cc7b59` ON `modrole` (`guild_id`);
    CREATE INDEX `idx_repros_report__c7a8a7` ON `repros` (`report_id`);
    CREATE INDEX `idx_trustedrole_guild_i_deb2b1` ON `trustedrole` (`guild_id`);
    CREATE INDEX `idx_userpermiss_guild_i_3a0dc1` ON `userpermission` (`guild_id`);
    CREATE INDEX `idx_watchedemoj_watcher_a04b30` ON `watchedemoji` (`watcher_id`);
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    ALTER TABLE `oreomap` COLLATE = utf8mb4_0900_ai_ci;
        """
