export interface ChatMessage extends BaseEntity {
  content: string
  role: string
  session: ChatSession
  validStatus: 'VALID' | 'INVALID'
}

export interface ChatSession extends BaseEntity {
  topic: string
  statistic: Statistic
  messages: ChatMessage[]
  createdBy: User
  validStatus: 'VALID' | 'INVALID' //有效或者无效
}
export interface Statistic {
  chatCount: number  //表示聊天次数
  tokenCount: number  //表示令牌数量
  wordCount: number  //表示单词数量
}

export interface ChatConfig extends BaseEntity {
  model: number
  temperature: number
  maxTokens: number
  presencePenalty: number
  apiKey: string
  createdBy: User
  validStatus: 'VALID' | 'INVALID'
}

export interface User extends BaseEntity {
  avatar: string  //表示用户的头像，通常是用户的个人资料图片或视觉表示的链接或引用。
  nickname: string  //表示用户的昵称，是用户在更友好或非正式场合下使用的名称
  username: string
  password: string
}
export class LoginResponse {
  tokenName: string
  tokenValue: string
  loginId: string
}

export type EditMode = 'CREATE' | 'EDIT'

export interface MyFile {
  name: string
  path: string
  status: 'ready' | 'uploading' | 'finish'
  file?: File
}

export interface QueryRequest<T> {
  pageNum: number
  pageSize: number
  keyword?: string
  query?: Partial<T>
}

export interface Page<T> {
  list: T[]
  total: number
  pageSize: number
  pageNum: number
  totalPages: number
}

export interface Result<T> {
  code: number
  success?: boolean
  msg: string
  result: T
}

export interface BaseEntity {
  id: string  //表示实体的唯一标识符，通常用于唯一标识数据库表中的记录或对象。
  updatedAt: string  //表示实体的最近更新时间，通常记录实体对象的最后一次更新时间戳。
  createdAt: string  //表示实体的创建时间，通常记录实体对象的创建时间戳。
  validStatus: 'VALID' | 'INVALID'
}
