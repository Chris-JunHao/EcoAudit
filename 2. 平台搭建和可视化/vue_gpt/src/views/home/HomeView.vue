<!--<script lang="ts" setup>-->
<!--import { onMounted, ref } from 'vue'-->
<!--import { ChatMessage, ChatSession } from '../../../typings'-->
<!--import { findChatSessionById, queryChatSession, saveChatSession } from '@/api/chat-session'-->
<!--import SessionItem from '@/views/home/components/SessionItem.vue'-->
<!--import { CirclePlus, Close, EditPen } from '@element-plus/icons-vue'-->
<!--import MessageRow from '@/views/home/components/MessageRow.vue'-->
<!--import MessageInput from '@/views/home/components/MessageInput.vue'-->
<!--import { Client } from '@stomp/stompjs'-->
<!--import dayjs from 'dayjs'-->
<!--import TextLoading from './components/TextLoading.vue'-->
<!--declare var Promise: any;-->

<!--const isEdit = ref(false)-->
<!--const activeSession = ref({ messages: {} } as ChatSession)-->
<!--// const sessionList = ref([] as ChatSession[])-->
<!--const sessionList = ref([-->
<!--    {-->
<!--        topic: '旅游问答',-->
<!--        statistic: {-->
<!--            // 统计数据的属性，可以自行填充-->
<!--            chatCount: 18-->
<!--        },-->
<!--    //     messages: [-->
<!--    //         {-->
<!--    //             content: '你好',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '这里是旅慧智库，有什么可以帮助你的？',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '我五一想去北京游玩一下，可以给我介绍几个著名旅游景点吗？',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '当然可以啊，可以游玩的景点有天安门广场，北海公园和天坛等等。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '可以展开说说天安门吗',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '天安门广场位于北京市中心，是中国甚至世界上最大的城市广场之一。广场的规模和设计体现了我国建筑风格的宏伟气势，同时是中国共产党中央委员会、中华人民共和国中央人民政府为举行重大国事和重要活动的专用场所。天安门广场的规划建设始于1949年10月1日，与1954年10月1日正式开放，1986年11月1日重新开放。天安门基座和基础都采用黄色砂岩修筑的黄色建筑，因此被称作“黄砖广场”。北京作为中国的首都，具有不同于其他城市的特殊象征功能，天安门作为北京和中国的标志，具有非常特殊的历史和文化价值。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '那北海公园呢？',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '北海公园和天坛都是明清时期的皇家园林，两个地方距离天安门广场很近，经常有人一起去游览。北海公园内既有历史悠久的建筑，也有美丽的湖泊和绿树花卉，游览时间一般来说为2-3小时左右。而天坛则是一个牺牲祭祀的场所，没有任何宗教信仰的人，是不允许进入天坛的，现在天坛已经变成了一座公园，免费开放，可以进去游览。天坛的皇家园林建筑里面，最著名的就是三大殿，即紫禁城内的太和殿、中和殿和保和殿。三大殿是整个公园的核心建筑，也是整个公园的代表建筑。太和殿是 广场中最大的殿，是皇帝举行重大庆典和朝见重要外宾的地方，里面有巨大的雕刻和壁画，非常壮观。中和殿比太和殿小一些，是皇帝 举行 盛大庆典的地方。保和殿比前两个小一些，是皇帝举行重要庆典的地方，也是重要的祭祀场所。除了三大殿外，还有一些重要的殿宇和皇帝御床过关之处，其中的神殿是保存完整的，也可以进去看看。  除了三大殿外，三大殿周围的区域，还有御园、神厨、御马厂和历史文物陈列展，可以看看。但是这三个地方都比较大，走下来也要差不多2小时左右，看否得看。  周边的景点也比较多，比如天安门城楼、北海公园对称的建筑、北京图书大厦等，都可以看看。  如果已经走了很远，也可以去逛逛天坛公园，开放免费。如果有点累，在这里逛一两个小时也不错。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '你知道火凤凰重庆火锅这家店吗?',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '当然知道，火凤凰重庆火锅位于东城区，是一家火锅店，下面是有关这家店的介绍: 聘请正宗重庆口味，秘制香料配比，高性价比是一家。主打的是牛蛙火锅，分为带皮和不带皮的两种牛蛙，加上宽粉以及各种蔬菜。店内的环境不用太讲究，吃的就是个味道。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '你能告诉我火凤凰重庆火锅(东直门店)这家店的评分吗?',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '这家店评分大概在4.7左右。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '这家店具体地址在哪?',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '在北京市东城区东直门内大街15-8号。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '这家店的营业时间呢?',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '营业时间为：全年 11:00-03:00。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '人均消费大概多少?',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '人均消费大约为150元。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         }-->
<!--    //     ],-->
<!--    //     createdBy: {-->
<!--    //         // 创建用户的属性，可以自行填充-->
<!--    //         avatar: '123',  //表示用户的头像，通常是用户的个人资料图片或视觉表示的链接或引用。-->
<!--    //         nickname: '456',  //表示用户的昵称，是用户在更友好或非正式场合下使用的名称-->
<!--    //         username: '789',-->
<!--    //         password: '10'-->
<!--    //     },-->
<!--    //     validStatus: 'VALID'-->
<!--    // },-->
<!--    // {-->
<!--    //     topic: '北京书籍',-->
<!--    //     statistic: {-->
<!--    //         // 统计数据的属性，可以自行填充-->
<!--    //         chatCount: 2-->
<!--    //     },-->
<!--    //     messages: [-->
<!--    //         {-->
<!--    //             content: '可以给我一些猫城记的简介吗？',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '下面是关于猫城记的介绍:“小猫儿，俏中来，到得那：花市火光连天，十字街头人来人往。”这是老舍先生所著的经典小说《猫城记》，讲述的是儿时回忆中的猫城故事。九·一八事变的第二年，33岁的老舍发表长篇讽刺小说《猫城记》，借火星上一座荒诞的猫城，述说了他眼中彼时中国的真相。由于“对人性超越时代的洞察”，《猫城记》在海外是知名度仅次于《骆驼祥子》的老舍作品，有日、法、英、德、俄、匈语六种译本。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '猫城记的读者评价怎么样呢？',-->
<!--    //             role: 'user',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         },-->
<!--    //         {-->
<!--    //             content: '这本书的评价有：看似辛辣痛快的讽刺，实则是浸入骨髓的深刻的绝望。',-->
<!--    //             role: 'right',-->
<!--    //             session: null, // 需要根据实际情况指定值-->
<!--    //             validStatus: 'VALID'-->
<!--    //         }-->
<!--    //     ],-->
<!--        createdBy: {-->
<!--            // 创建用户的属性，可以自行填充-->
<!--        },-->
<!--        validStatus: 'VALID'-->
<!--    }-->
<!--]);-->
<!--onMounted(() => {-->
<!--    // 查询自己的聊天会话-->
<!--    queryChatSession({ pageSize: 1000, pageNum: 1, query: {} }).then((res) => {-->
<!--        // 讲会话添加到列表中-->
<!--        sessionList.value.push(...res.result.list)-->
<!--        // 默认选中的聊天会话是第一个-->
<!--        if (sessionList.value.length > 0) {-->
<!--            activeSession.value = sessionList.value[0]-->
<!--        }-->
<!--    })-->
<!--})-->
<!--// 切换会话-->
<!--const handleSessionSwitch = (session: ChatSession) => {-->
<!--    activeSession.value = session-->
<!--}-->
<!--// 从会话列表中删除会话-->
<!--const handleDeleteSession = (session: ChatSession) => {-->
<!--    const index = sessionList.value.findIndex((value) => {-->
<!--        return value.id === session.id-->
<!--    })-->
<!--    sessionList.value.splice(index, 1)-->
<!--}-->
<!--// 新增会话-->
<!--const handleCreateSession = async () => {-->
<!--    const res = await saveChatSession({ topic: '新的聊天' })-->
<!--    sessionList.value.unshift((await findChatSessionById(res.result)).result)-->
<!--}-->
<!--const handleUpdateSession = () => {-->
<!--    saveChatSession(activeSession.value)-->
<!--    isEdit.value = false-->
<!--}-->

<!--const client = new Client({-->
<!--    brokerURL: 'ws://localhost:8080/handshake',-->
<!--    onConnect: () => {-->
<!--        // 连接成功后订阅ChatGPT回复地址-->
<!--        client.subscribe('/user/queue/chatMessage/receive', (message) => {-->
<!--            // 将每次回复的结果追加到回复结果中-->
<!--            responseMessage.value.content += message.body-->
<!--            console.log(message.body)-->
<!--        })-->
<!--    }-->
<!--})-->
<!--// 发起连接-->
<!--client.activate()-->
<!--// ChatGPT的回复-->
<!--const responseMessage = ref({} as ChatMessage)-->
<!--const handleSendMessage = (message: string) => {-->
<!--    // 新建一个ChatGPT回复对象，不能重复使用同一个对象。-->
<!--    responseMessage.value = {-->
<!--        role: 'assistant',-->
<!--        content: '',-->
<!--        // 因为回复的消息没有id，所以统一将创建时间+index当作key-->
<!--        createdAt: dayjs().format('YYYY-MM-DD HH:mm:ss')-->
<!--    } as ChatMessage-->
<!--    // 用户的提问-->
<!--    const chatMessage = {-->
<!--        session: Object.assign({}, activeSession.value),-->
<!--        content: message,-->
<!--        role: 'user',-->
<!--        createdAt: dayjs().format('YYYY-MM-DD HH:mm:ss')-->
<!--    } as ChatMessage-->
<!--    // 防止循环依赖，会导致json序列化失败-->
<!--    chatMessage.session.messages = []-->
<!--    client.publish({-->
<!--        destination: '/socket/chatMessage/send',-->
<!--        body: JSON.stringify(chatMessage)-->
<!--    })-->
<!--    // 将两条消息显示在页面中-->
<!--    activeSession.value.messages.push(...[chatMessage, responseMessage.value])-->
<!--}-->
<!--</script>-->

<!--<template>-->
<!--    &lt;!&ndash; 最外层页面于窗口同宽，使聊天面板居中 &ndash;&gt;-->
<!--    <div class="home-view">-->
<!--        &lt;!&ndash; 整个聊天面板 &ndash;&gt;-->
<!--        <div class="chat-panel">-->
<!--            &lt;!&ndash; 左侧的会话列表 &ndash;&gt;-->
<!--            <div class="session-panel">-->
<!--                <div class="title">旅慧智库</div>-->
<!--                <div class="description">构建你的旅途智能</div>-->
<!--                <div class="session-list">-->
<!--                    &lt;!&ndash; for循环遍历会话列表用会话组件显示，并监听点击事件和删除事件。点击时切换到被点击的会话，删除时从会话列表中提出被删除的会话。 &ndash;&gt;-->
<!--                    &lt;!&ndash;  &ndash;&gt;-->
<!--                    <SessionItem v-for="session in sessionList" :key="session.id"-->
<!--                        :active="session.id === activeSession.id" :session="session" class="session"-->
<!--                        @click="handleSessionSwitch(session)" @delete="handleDeleteSession"></SessionItem>-->
<!--                </div>-->
<!--                <div class="button-wrapper">-->
<!--                    <div class="new-session">-->
<!--                        <el-button @click="handleCreateSession">-->
<!--                            <el-icon :size="15" class="el-icon&#45;&#45;left">-->
<!--                                <CirclePlus />-->
<!--                            </el-icon>-->
<!--                            新的聊天-->
<!--                        </el-button>-->
<!--                    </div>-->
<!--                </div>-->
<!--            </div>-->
<!--            &lt;!&ndash; 右侧的消息记录 &ndash;&gt;-->
<!--            <div class="message-panel">-->
<!--                &lt;!&ndash; 会话名称 &ndash;&gt;-->
<!--                <div class="header">-->
<!--                    <div class="front">-->
<!--                        &lt;!&ndash; 如果处于编辑状态则显示输入框让用户去修改 &ndash;&gt;-->
<!--                        <div v-if="isEdit" class="title">-->
<!--                            &lt;!&ndash; 按回车代表确认修改 &ndash;&gt;-->
<!--                            <el-input v-model="activeSession.topic" @keydown.enter="handleUpdateSession"></el-input>-->
<!--                        </div>-->
<!--                        &lt;!&ndash; 否则正常显示标题 &ndash;&gt;-->
<!--                        <div v-else class="title">{{ activeSession.topic }}</div>-->
<!--                        <div class="description">与旅游小助手的{{ activeSession.messages.length }}条对话</div>-->
<!--                    </div>-->
<!--                    &lt;!&ndash; 尾部的编辑按钮 &ndash;&gt;-->
<!--                    <div class="rear">-->
<!--                        <el-icon :size="20">-->
<!--                            &lt;!&ndash; 不处于编辑状态显示编辑按钮 &ndash;&gt;-->
<!--                            <EditPen v-if="!isEdit" @click="isEdit = true" />-->
<!--                            &lt;!&ndash; 处于编辑状态显示取消编辑按钮 &ndash;&gt;-->
<!--                            <Close v-else @click="isEdit = false"></Close>-->
<!--                        </el-icon>-->
<!--                    </div>-->
<!--                </div>-->
<!--                <el-divider :border-style="'solid'" class="border" />-->
<!--                <div class="message-list">-->
<!--                    &lt;!&ndash; 过渡效果 &ndash;&gt;-->
<!--                    <transition-group name="list">-->
<!--                        <message-row v-for="(message, index) in activeSession.messages" :key="message.createdAt + index"-->
<!--                            :avatar="activeSession.createdBy.avatar" :message="message"></message-row>-->
<!--                        &lt;!&ndash; <TextLoading></TextLoading> &ndash;&gt;-->
<!--                    </transition-group>-->
<!--                </div>-->
<!--                &lt;!&ndash; 监听发送事件 &ndash;&gt;-->
<!--                <div class="message-input-in">-->
<!--                    <message-input @send="handleSendMessage"></message-input>-->
<!--                </div>-->

<!--            </div>-->
<!--        </div>-->
<!--    </div>-->
<!--</template>-->

<!--<style lang="scss" scoped>-->
<!--.home-view {-->
<!--    width: 100vw;-->
<!--    height: calc(90vh - 19px);-->
<!--    display: flex;-->
<!--    justify-content: center;-->
<!--    padding-top: 30px;-->

<!--    // &lt;!&ndash; 整个聊天面板 &ndash;&gt;-->
<!--    .chat-panel {-->
<!--        width: 65%;-->
<!--        height: 90%;-->
<!--        display: flex;-->
<!--        border-radius: 20px; //圆角效果-->
<!--        background-color: white;-->
<!--        box-shadow: 0 0 20px 20px rgba(black, 0.05); //添加元素的阴影效果-->


<!--        // &lt;!&ndash; 左侧的会话列表 &ndash;&gt;-->
<!--        .session-panel {-->
<!--            min-width: 100px;-->
<!--            width: 30%;-->
<!--            height: calc(100% - 40px); //剪掉的40px是左侧会话的上下内边距-->
<!--            border-top-left-radius: 20px;-->
<!--            border-bottom-left-radius: 20px;-->
<!--            padding: 20px;-->
<!--            position: relative;-->
<!--            border-right: 1px solid rgba(black, 0.07);-->
<!--            background-color: rgb(60, 99, 117);-->

<!--            /* 标题 */-->
<!--            .title {-->
<!--                margin-top: 20px;-->
<!--                font-size: 20px;-->
<!--            }-->

<!--            /* 描述*/-->
<!--            .description {-->
<!--                color: rgba(black, 0.7);-->
<!--                font-size: 14px;-->
<!--                margin-top: 10px;-->
<!--            }-->

<!--            .session-list {-->
<!--                .session {-->
<!--                    /* 每个会话之间留一些间距 */-->
<!--                    margin-top: 20px;-->
<!--                }-->
<!--            }-->

<!--            .button-wrapper {-->
<!--                /* session-panel是相对布局，这边的button-wrapper是相对它绝对布局 */-->
<!--                position: absolute;-->
<!--                bottom: 20px;-->
<!--                left: 0;-->
<!--                display: flex;-->
<!--                /* 让内部的按钮显示在右侧 */-->
<!--                justify-content: flex-end;-->
<!--                /* 宽度和session-panel一样宽*/-->
<!--                width: 100%;-->

<!--                /* 按钮于右侧边界留一些距离 */-->
<!--                .new-session {-->
<!--                    margin-right: 20px;-->
<!--                }-->
<!--            }-->
<!--        }-->

<!--        /* 右侧消息记录面板*/-->
<!--        .message-panel {-->
<!--            width: 70%;-->
<!--            height: calc(100% - 110px);-->

<!--            .header {-->
<!--                height: 15%;-->
<!--                padding: 20px 20px 0 20px;-->
<!--                /* 上、右、下、左 */-->
<!--                display: flex;-->
<!--                /* 会话名称和编辑按钮在水平方向上分布左右两边 */-->
<!--                justify-content: space-between;-->

<!--                /* 前部的标题和消息条数 */-->
<!--                .front {-->
<!--                    .title {-->
<!--                        color: rgba(black, 0.7);-->
<!--                        font-size: 20px;-->
<!--                    }-->

<!--                    .description {-->
<!--                        margin-top: 10px;-->
<!--                        color: rgba(black, 0.5);-->
<!--                    }-->
<!--                }-->

<!--                /* 尾部的编辑和取消编辑按钮 */-->
<!--                .rear {-->
<!--                    display: flex;-->
<!--                    align-items: center;-->
<!--                }-->
<!--            }-->

<!--            .border {-->
<!--                padding: 0px;-->
<!--                margin: 10px 0px 10px 0px;-->
<!--            }-->

<!--            .message-list {-->
<!--                height: 60%; //聊天框的高度-->
<!--                padding: 15px;-->
<!--                // 消息条数太多时，溢出部分滚动-->
<!--                overflow-y: scroll;-->

<!--                // 当切换聊天会话时，消息记录也随之切换的过渡效果-->
<!--                .list-enter-active,-->
<!--                .list-leave-active {-->
<!--                    transition: all 0.5s ease;-->
<!--                }-->

<!--                .list-enter-from,-->
<!--                .list-leave-to {-->
<!--                    opacity: 0;-->
<!--                    transform: translateX(30px);-->
<!--                }-->
<!--            }-->

<!--            .message-input-in {-->
<!--                width: auto;-->
<!--                height: 25%;-->
<!--                padding: 10px;-->
<!--                bottom: 0px;-->
<!--            }-->
<!--        }-->
<!--    }-->
<!--}-->

<!--</style>-->
<!--<template>-->
<!--  <div class="main-page">-->
<!--    <div class="layout">-->
<!--      <div class="province-list">-->
<!--        <h2>省份选择</h2>-->
<!--        <ul>-->
<!--          <li v-for="province in provinces" :key="province.name">-->
<!--            <el-button @click="handleProvinceClick(province.name)">-->
<!--              {{ province.name }} - 水质: {{ province.data.waterQuality }}-->
<!--            </el-button>-->
<!--          </li>-->
<!--        </ul>-->
<!--      </div>-->

<!--      <div class="map-container">-->
<!--        &lt;!&ndash; 直接显示地图图片 &ndash;&gt;-->
<!--        <img src="@/assets/home/img.png" alt="中国地图" style="width: 100%; height: 100%;" />-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<style scoped>-->
<!--.main-page {-->
<!--  display: flex;-->
<!--  flex-direction: row;-->
<!--  height: 100vh;-->
<!--  justify-content: center;-->
<!--  padding: 20px;-->
<!--}-->

<!--.layout {-->
<!--  display: flex;-->
<!--  flex-direction: row;-->
<!--  width: 100%;-->
<!--}-->

<!--.province-list {-->
<!--  width: 30%;-->
<!--  padding: 20px;-->
<!--  background-color: #f4f4f4;-->
<!--  border-right: 1px solid #ccc;-->
<!--}-->

<!--.map-container {-->
<!--  width: 70%;-->
<!--  padding: 20px;-->
<!--}-->
<!--</style>-->



<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 路由实例
const router = useRouter()

// 静态的省份数据
const provinces = ref([
  { name: '北京', waterQuality: '优' },
  { name: '上海', waterQuality: '良' },
  { name: '广东', waterQuality: '中' },
  { name: '浙江', waterQuality: '优' },
  { name: '四川', waterQuality: '良' }
])

// 点击省份后的处理函数，跳转到省份详情页
const handleProvinceClick = (provinceName: string) => {
  router.push(`/province/${provinceName}`)
}

</script>

<template>
  <div class="main-page">
    <div class="layout">
      <!-- 左侧省份列表 -->
      <div class="province-list">
        <h2>省份选择</h2>
        <ul>
          <li v-for="province in provinces" :key="province.name">
            <el-button @click="handleProvinceClick(province.name)">
              {{ province.name }} - 水质: {{ province.waterQuality }}
            </el-button>
          </li>
        </ul>
      </div>

      <!-- 右侧地图图片展示 -->
      <div class="map-container">
        <img src="@/assets/home/img.png" alt="中国地图" class="china-map" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-page {
  display: flex;
  flex-direction: row;
  height: 100vh;
  justify-content: center;
  padding: 20px;
}

.layout {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.province-list {
  width: 30%;
  padding: 20px;
  background-color: #f4f4f4;
  border-right: 1px solid #ccc;

  h2 {
    text-align: center;
    margin-bottom: 20px;
  }

  ul {
    list-style: none;
    padding: 0;

    li {
      margin: 10px 0;
    }
  }

  button {
    width: 100%;
  }
}

.map-container {
  width: 70%;
  padding: 20px;
}

.china-map {
  width: 100%;
  height: auto;
}
</style>
