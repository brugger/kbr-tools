export class Acl {
  id:string;
  endpoint:string;
  can_create:boolean;
  can_read:boolean;
  can_update:boolean;
  can_delete:boolean;
}

export class UserInfo {
  id: string;
  username: string;
  email: string;
  superuser: boolean;
  name: string;
  acls: Acl[];
}

